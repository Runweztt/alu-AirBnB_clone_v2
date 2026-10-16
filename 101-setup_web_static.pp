# Configure a server for deployment of AirBnB static content.

package { 'nginx':
  ensure => installed,
}

file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => Package['nginx'],
}

file { '/data/web_static':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => File['/data'],
}

file { '/data/web_static/releases':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => File['/data/web_static'],
}

file { '/data/web_static/shared':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => File['/data/web_static'],
}

file { '/data/web_static/releases/test':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => File['/data/web_static/releases'],
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => "Holberton School\n",
  require => File['/data/web_static/releases/test'],
}

file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  force   => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test'],
}

file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {\n    listen 80 default_server;\n    listen [::]:80 default_server;\n    server_name _;\n\n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }\n}\n",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}
