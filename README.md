# Flatpak update checker

Small utility to check updates for flatpak installed apps.

# How to use

This needs Python 3.5 or newer installed, and it uses the `flatpak` cli
to get the information. It doesn't have any other external dependency.

# Example run

```
$ ./flatpak-check-updates.py
com.github.xournalpp.xournalpp: 1.1.3 -> 1.1.3 [rebuild]
org.freedesktop.Platform.GL.default: 23.1.1 -> 21.3.9 [update]
org.freedesktop.Platform.VAAPI.Intel:  ->  [unknown]
org.freedesktop.Platform: 22.08.12.1 -> 21.08.18 [update]
org.gnome.Platform:  ->  [unknown]
```

Each app is "tagged" with a word,
* update: there's a new version of the app
* rebuild: there's an update available but the application version is the same
as the locally installed one. This means that there was a change on the
flatpak itself and the app was rebuilt, there's not a new version/release of
the app.
* unknown: flatpak lists some apps with no version, I don't know what that
means, possibly that they are not versioned with a number as other apps.


# Note
At the time of writing this, there was not an official way of easily doing
this.

See: https://github.com/flatpak/flatpak/issues/729,
https://github.com/flatpak/flatpak/pull/985,
https://github.com/flatpak/flatpak/issues/3685
