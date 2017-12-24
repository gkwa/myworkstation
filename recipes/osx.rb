include_recipe 'homebrew'

homebrew_tap 'caskroom/cask'
homebrew_tap 'homebrew/completions'
homebrew_tap 'homebrew/core'
homebrew_tap 'homebrew/dupes'
homebrew_tap 'homebrew/fuse'
homebrew_tap 'homebrew/gui'
homebrew_tap 'homebrew/php'
homebrew_tap 'homebrew/python'
homebrew_tap 'homebrew/science'
homebrew_tap 'homebrew/services'
homebrew_tap 'homebrew/versions'
homebrew_tap 'homebrew/x11'
homebrew_tap 'neovim/neovim'

node['myworkstation']['packages'].each do |package|
  package package do
    action :install
    ignore_failure true
  end
end
