# buildozer.spec
[app]
title = Book Exchange
package.name = bookexchange
package.domain = org.bookexchange
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,kivy_garden.mapview,opencv-python,pyzbar
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0
android.permissions = INTERNET,ACCESS_FINE_LOCATION,CAMERA
android.api = 29
android.minapi = 21
android.sdk = 24
android.ndk = 23b
android.accept_sdk_license = True
