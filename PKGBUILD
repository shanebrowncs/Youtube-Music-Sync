# Maintainer: Shane "SajeOne" Brown <contact@shane-brown.ca>
pkgname=youtube-sync
pkgver=1.0.1
pkgrel=1
pkgdesc="Maintains a local repository of music from a YouTube playlist"
arch=('any')
url="https://github.com/SajeOne/Youtube-Music-Sync"
license=('GPL')
depends=('python')
makedepends=('python-setuptools' 'youtube-dl')
optdepends=('python-mutagen: -t id3 tagging support')
provides=('youtube-sync')
source=("git+https://github.com/SajeOne/Youtube-Music-Sync")
md5sums=('SKIP')
_gitname="Youtube-Music-Sync"

package() {
  cd "$srcdir/$_gitname"
  python setup.py install --root="$pkgdir/" --optimize=1
}

# vim:set ts=2 sw=2 et:
