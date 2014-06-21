# Maintainer: Ondřej Hruška <ondra@ondrovo.com>

pkgname=adios-git
pkgver=5ea4e72
pkgrel=1
pkgdesc="Simple, versatile session exit dialog, inspired by cb-exit."
arch=('any')
url='https://github.com/MightyPork/adios'
license=('MIT')

depends=('python3' 'python-gobject')
makedepends=('git')

source=('git://github.com/MightyPork/adios.git')
provides=('adios')
md5sums=('SKIP')

pkgver() {
    cd "$srcdir/adios"
    git describe --always | sed 's|-|.|g'
}

package() {
  install -Dm 755 "$srcdir/adios/adios" "$pkgdir/usr/bin/adios"
}
