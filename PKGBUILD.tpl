# Maintainer: Ondřej Hruška <ondra@ondrovo.com>

pkgname=adios
pkgver=%version
pkgrel=%rel
pkgdesc="Simple, versatile session exit dialog, inspired by cb-exit."
arch=('any')
url='https://github.com/MightyPork/adios'
license=('MIT')

depends=('python3' 'python-gobject')
makedepends=('git')

source=('https://github.com/MightyPork/adios/releases/download/%version/release.tar.gz')
provides=('adios')
conflicts=('adios-git')
md5sums=('%md5')

package() {
  # install license
  install -D -m644 "$srcdir/LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
  
  # install files in /usr/share
  install -Dm 755 "$srcdir/*" "$pkgdir/usr/share/adios/"
  
  # install link in /usr/bin
  mkdir -p "${pkgdir}/usr/bin/"
  ln -s /usr/share/adios/adios "${pkgdir}/usr/bin/adios"
}
