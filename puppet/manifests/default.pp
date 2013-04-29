exec { "apt-update":
	command => "/usr/bin/apt-get update"
}

# create vagrant user and group
group { 'vagrant':
	ensure => 'present',
}
user { 'vagrant':
	password_min_age => '0',
	ensure => 'present',
	password_max_age => '99999',
	password => 'vagrant',
	gid => 'vagrant',
	groups => ['www-data','vagrant'],
	require => Group['vagrant'],
}

# make sure vagrant can access all site code
exec { "vagrant_access":
	command => "sudo chgrp -R vagrant /vagrant",
	path => "/usr/bin",
	require => Group["vagrant"],
}

stage { "pre": before => Stage["main"] }
class python {
	package {
		"build-essential": ensure => "purged";
		"python": ensure => "latest";
		"python-dev": ensure => "purged";
		"python-setuptools": ensure => "purged";
	}
	exec { "easy_install pip":
		path => "/usr/local/bin:/usr/bin:/bin",
		refreshonly => true,
		require => Package["python-setuptools"],
		subscribe => Package["python-setuptools"],
	}
}
class { "python": stage => "pre" }
 
package {
	"python-django":
		ensure => "latest",
		require => [Exec["apt-update"], Package["python-mysqldb"]];
	"libmysqlclient-dev":
	notify => Service["mysqld"],
		ensure => "latest";
	"python-mysqldb":
		notify => Service["mysqld"],
		ensure => "latest",
		require => [Package["mysql-server"], Package["libmysqlclient-dev"], Exec["apt-update"]];
	"python-django-debug-toolbar":
		ensure => "latest";
}
 
package {
	"apache2-mpm-worker":
		ensure => "latest";
	"libapache2-mod-wsgi":
		ensure => "latest";
}

package {
	"vim":
		ensure => "latest";
}

file { "/etc/apache2/ssl":
	ensure => "directory",
	require => Package["apache2-mpm-worker"],
}
file { "/etc/apache2/ssl/synapsie":
	ensure => "directory",
	require => File["/etc/apache2/ssl"],
}
 
file {
	"/etc/apache2/sites-available/synapsie.com":
		notify => Service["apache2"],
		content => template("/vagrant/puppet/manifests/apache/vhost.erb"),
		ensure => file,
		require => Package["apache2-mpm-worker"];
	"/etc/apache2/sites-enabled/001-synapsie.com":
		notify => Service["apache2"],
		ensure => "/etc/apache2/sites-available/synapsie.com",
		require => Package["apache2-mpm-worker"];
	"/etc/apache2/sites-enabled/000-default":
		notify => Service["apache2"],
		ensure => absent,
		require => Package["apache2-mpm-worker"];
	"/etc/apache2/mods-enabled/expires.load":
		notify => Service["apache2"],
		ensure => link,
		require => Package["apache2-mpm-worker"],
		target => '/etc/apache2/mods-available/expires.load';
	"/etc/apache2/mods-enabled/ssl.load":
		notify => Service["apache2"],
		ensure => link,
		require => Package["apache2-mpm-worker"],
		target => '/etc/apache2/mods-available/ssl.load';
	"/etc/apache2/ssl/synapsie/synapsie.com.crt":
		notify => Service["apache2"],
		content => template("/vagrant/puppet/manifests/apache/ssl/${settings::env}/synapsie.com.crt"),
		ensure => file,
		require => File["/etc/apache2/ssl/synapsie"],
		owner => "vagrant",
		group => "vagrant",
		mode => 644;
	"/etc/apache2/ssl/synapsie/synapsie.com.key":
		notify => Service["apache2"],
		content => template("/vagrant/puppet/manifests/apache/ssl/${settings::env}/synapsie.com.key"),
		ensure => file,
		require => File["/etc/apache2/ssl/synapsie"],
		owner => "root",
		group => "root",
		mode => 600;
	"/etc/apache2/ssl/synapsie/gd_bundle.crt":
		notify => Service["apache2"],
		content => template("/vagrant/puppet/manifests/apache/ssl/gd_bundle.crt"),
		ensure => file,
		require => File["/etc/apache2/ssl/synapsie"],
		owner => "vagrant",
		group => "vagrant",
		mode => 644;
	"/vagrant/apache/site.wsgi":
		notify => Service["apache2"],
		content => template("/vagrant/puppet/manifests/apache/wsgi/${settings::env}.wsgi"),
		ensure => file,
		require => Package["apache2-mpm-worker"],
		owner => "vagrant",
		group => "vagrant",
		mode => 644;
	"/vagrant/logs/error.log":
		ensure => file;
}

service { "apache2":
	enable => true,
	ensure => running,
	require => Package["apache2-mpm-worker"],
	subscribe => [
		Package[
			"apache2-mpm-worker",
			"libapache2-mod-wsgi"],
		File[
			"/etc/apache2/sites-available/synapsie.com",
			"/etc/apache2/sites-enabled/001-synapsie.com",
			"/etc/apache2/sites-enabled/000-default"]],
}

class { 'mysql': }

class { "mysql::server": 
	config_hash => { 'root_password' => 'password' }
}

mysql::db { 'database':
	name => 'dj_synapsie',
	charset => 'latin1',
	user     => 'dj_synapsie',
	password => 'syn.apsie.141',
	host     => 'localhost',
	grant    => ['all'],
	ensure   => present,
}

exec { "django_database_setup":
	cwd     => "/vagrant",
	command => "python manage.py syncdb --noinput",
	path    => "/usr/bin",
	require => [Database["dj_synapsie"], Database_user["dj_synapsie@localhost"], Service["mysqld"], Package["python"], Package["python-mysqldb"], Package["mysql-server"]],
}

# do a final build
exec { "build_synapsie_database":
	cwd     => "/vagrant",
	command => "python manage.py syncdb --noinput",
	path    => "/usr/bin",
	require => [Database["dj_synapsie"], Database_user["dj_synapsie@localhost"], Service["mysqld"], Package["python"], Package["python-mysqldb"], Package["mysql-server"]],
}
exec { "build_synapsie_code":
	cwd     => "/vagrant",
	command => "touch apache/site.wsgi",
	path    => "/usr/bin",
	require => [Group['vagrant'], Database["dj_synapsie"], Database_user["dj_synapsie@localhost"], Service["mysqld"], Package["python"], Package["python-mysqldb"], Package["mysql-server"]],
}