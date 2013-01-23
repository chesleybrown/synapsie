exec { "apt-update":
	command => "/usr/bin/apt-get update"
}

stage { "pre": before => Stage["main"] }
class python {
	package {
		"build-essential": ensure => "purged";
		"python": ensure => "2.7.3-0ubuntu2";
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
		ensure => "1.3.1-4ubuntu1.4",
		require => [Exec["apt-update"], Package["python-mysqldb"]];
	"libmysqlclient-dev":
		ensure => "latest";
	"python-mysqldb":
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
 
file {
	"/etc/apache2/sites-available/synapsie.com":
		content => template("/vagrant/puppet/manifests/vhost.erb"),
		ensure => file,
		require => Package["apache2-mpm-worker"];
	"/etc/apache2/sites-enabled/001-synapsie.com":
		ensure => "/etc/apache2/sites-available/synapsie.com",
		require => Package["apache2-mpm-worker"];
	"/etc/apache2/sites-enabled/000-default":
		ensure => absent,
		require => Package["apache2-mpm-worker"];
	"/etc/apache2/mods-enabled/expires.load":
		ensure => link,
		require => Package["apache2-mpm-worker"],
		target => '/etc/apache2/mods-available/expires.load';
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
	command => "python manage.py syncdb",
	path    => "/usr/bin",
	require => [Package["python"], Package["python-mysqldb"], Package["mysql-server"]],
}