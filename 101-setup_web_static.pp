# Install Nginx if not already installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories if they don't exist
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

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "Fake content\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test'],
}

# Create a symbolic link /data/web_static/current
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  force   => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test/index.html'],
}

# Give ownership of /data/ folder to the ubuntu user and group recursively
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Update Nginx configuration to serve the content of /data/web_static/current to hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
