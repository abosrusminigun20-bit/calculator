[app]

# Название под иконкой (если сборка ругается на кириллицу — замените на Calculator)
title = Калькулятор
package.name = calculator
package.domain = org.example

source.dir = .
source.include_exts = py

version = 1.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
