# Maintainer: Ondřej Hruška <ondra@ondrovo.com>

pkgname=adios
pkgver=0.2.0
pkgrel=1
pkgdesc="Simple, versatile session exit dialog, inspired by cb-exit."
arch=('any')
url='https://github.com/MightyPork/adios'
license=('MIT')

depends=('python3' 'python-gobject')
makedepends=('git')

source=('https://github.com/MightyPork/adios/archive/0.2.tar.gz')
provides=('adios')
#md5sums=('SKIP')

package() {
  install -Dm 755 "$srcdir/adios/src/adios.py" "$pkgdir/usr/bin/adios"
}
