# Maintainer: Max Bruckner
pkgname=adios-git
pkgver=0.1
pkgrel=1
pkgdesc="Simple, versatile session exit dialog, based on cb-exit."
arch=('any')
url='https://github.com/MightyPork/exit-prompt'
license=('MIT')

depends=('python3' 'python-gobject')
makedepends=('git')

source=('git://github.com/MightyPork/exit-prompt.git')
provides=('adios')
md5sums=('SKIP')

pkgver() {
    cd "$srcdir/adios"
    git describe --always | sed 's|-|.|g'
}

package() {
  install -Dm 755 "$srcdir/exit-prompt/adios" "$pkgdir/usr/bin/adios"
}
