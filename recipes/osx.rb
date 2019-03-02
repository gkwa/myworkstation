include_recipe 'homebrew'

execute 'brew packages' do
  command 'brew install ack apr apr-util asciidoc aspcud aspell atk atkmm augeas autoconf automake autossh aws-cfn-tools aws-elasticache awscli azure-cli bash bash-completion bats bazaar bazel bazel bdw-gc blackbox boost boost-build bower bsdiff bup c-ares cadaver cairo cairomm camlp4 cassandra cdrtools chrome-cli clasp clingo cloog018 cloud-watch cmake consul-template coreutils crunch ctags cunit curl cython d-bus dbus dep dialog dirmngr dnsmasq docbook docker docker-machine docker-machine-driver-xhyve dos2unix dpkg duck duck dvm dvm easy-tag ec2-ami-tools ec2-api-tools editorconfig eigen elasticsearch elinks emacs enscript entr etcd exa exercism faad2 ffmpeg findutils fish flac fontconfig fping fpp freerdp freetype fribidi fswatch fzf gawk gdbm gdk-pixbuf geckodriver geoip gettext ghc giflib gist git git-extras git-lfs git-series git-when-merged gitversion glib glibmm gmp gnu-getopt gnu-indent gnu-sed gnu-tar gnupg gnupg2 gnutls go-bindata goaccess gobject-introspection golang gpatch gpgme gradle graphite2 graphviz grep gringo groovy gsettings-desktop-schemas gsl gtk+ gtk+3 gtkmm guile harfbuzz hicolor-icon-theme highlight htop-osx httpd httpie hub hugo icu4c id3lib iftop ilmbase imagemagick intltool iproute2mac irssi isl jansson jemalloc jpeg jq jsonnet jsonpp juju kops kqwait kubectx kubernetes-cli kubernetes-helm lame ledger leptonica little-cms lsof lua luajit lynx lzo make makedepend maven mitmproxy mobile-shell mono mosh msgpack mtr mutt n ncdu neon neovim neovim nethogs nettle nghttp2 nginx nload nmap node npth nvm ocaml ocamlbuild oniguruma opam opencore-amr openexr openjpeg openssl openssl openvpn opus p11-kit p7zip packer pango pangomm parallel patchutils pcre pcre2 perl pidof pinentry pipenv pixman pkg-config popt protobuf psgrep pssh pth pyenv pyenv-virtualenv pyenv-virtualenvwrapper python python3 qemu qt ranger rbenv rdesktop re2c readline reattach-to-user-namespace recode redo restic rpm2cpio rsync rtmpdump rubberband ruby-build rust s-lang scons selenium-server-standalone snappy source-highlight spdylay speex sphinx-doc sqlite squid ssh-copy-id sshuttle stow subversion taglib terminal-notifier terraform terraforming tesseract texi2html the_silver_searcher theora tig timewarrior tmux tokyo-cabinet travis tree unbound unibilium unixodbc utf8proc vault vde vim watch watchman wavpack wdiff webp wemux wget wiggle winexe wireshark x264 x265 xhyve xml-coreutils xmlstarlet xvid xz yajl yarn yasm yq'
  user 'travis'
end

execute 'brew packages' do
  command 'brew cask install alfred amethyst charles chromedriver cyberduck docker dropbox firefox google-chrome google-cloud-sdk hammerspoon intellij-idea iterm2 kindle minikube mongodb mysql-shell neo4j phantomjs postman powershell pycharm screenflick slack spectacle the-unarchiver tunnelblick vagrant virtualbox virtualbox-extension-pack visual-studio-code vlc xquartz'
  user 'travis'
end

package "Instll 2 packages at once" do
  action :install
  ignore_failure true
  package_name %( confuse colordiff )
end

homebrew_tap 'azure/draft'
package 'azure/draft/draft' do
  action :install
  ignore_failure true
end

homebrew_tap 'habitat-sh/habitat'
package 'hab' do
  action :install
  ignore_failure true
end
