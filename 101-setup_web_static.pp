package { 'nginx':
  ensure => installed,
}

file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { ['/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  require => File['/data'],
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "Fake content\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test'],
}

file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  force   => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test/index.html'],
}

file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  require => Package['nginx'],
  notify  => Service['nginx'],
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
