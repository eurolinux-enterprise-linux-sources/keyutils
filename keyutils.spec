%define vermajor 1
%define version %{vermajor}.4
%define libdir /%{_lib}
%define usrlibdir %{_prefix}/%{_lib}
%define libapivermajor 1
%define libapiversion %{libapivermajor}.3

Summary: Linux Key Management Utilities
Name: keyutils
Version: %{version}
Release: 5%{?dist}
# The main package is GPLv2+ and -libs/-libs-devel are LGPLv2+
License: GPLv2+ and LGPLv2+
Group: System Environment/Base
ExclusiveOS: Linux
Url: http://people.redhat.com/~dhowells/keyutils/

Source0: http://people.redhat.com/~dhowells/keyutils/keyutils-%{version}.tar.bz2
Patch1: keyutils-1.4-keytype-specific-file.patch

# Fix max depth of key tree dump (67e435c3f1810bc0902698ea4ac4a85b4aef7e4f)
Patch2: keyutils-1.4-keyctl-show.patch

# Show more key serial ID digits in show command (part c2bba5a9f8f50b22f736ec262504229a719bcfce)
Patch3: keyutils-1.4-keyctl-show-2.patch

# Fix the input buffer size for padd and pinstantiate (df5cab5362695b92896a41a86556e9dad156419d)
Patch4: keyutils-1.4-keyctl-padd.patch

# Fix the keyctl padd command and similar to handle binary data on stdin (d4dea943947ffe91d3ba1fe05e84fa4c8f46fcdd)
Patch5: keyutils-1.4-keyctl-padd-2.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glibc-kernheaders >= 2.4-9.1.92
Requires: keyutils-libs == %{version}-%{release}

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to user space to get a key
instantiated.

%package libs
Summary: Key utilities library
Group: System Environment/Base

%description libs
This package provides a wrapper library for the key management facility system
calls.

%package libs-devel
Summary: Development package for building Linux key management utilities
Group: System Environment/Base
Requires: keyutils-libs == %{version}-%{release}

%description libs-devel
This package provides headers and libraries for building key utilities.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
make \
	NO_ARLIB=1 \
	LIBDIR=%{libdir} \
	USRLIBDIR=%{usrlibdir} \
	RELEASE=.%{release} \
	NO_GLIBC_KEYERR=1 \
	CFLAGS="-Wall $RPM_OPT_FLAGS -Wl,-z,relro"

%install
rm -rf $RPM_BUILD_ROOT
make \
	NO_ARLIB=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{libdir} \
	USRLIBDIR=%{usrlibdir} \
	install

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README LICENCE.GPL
/sbin/*
/bin/*
/usr/share/keyutils
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%config(noreplace) /etc/*

%files libs
%defattr(-,root,root,-)
%doc LICENCE.LGPL
%{libdir}/libkeyutils.so.%{libapiversion}
%{libdir}/libkeyutils.so.%{libapivermajor}

%files libs-devel
%defattr(-,root,root,-)
%{usrlibdir}/libkeyutils.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Wed Mar 12 2014 David Howells  <dhowells@redhat.com> - 1.4-5
- Make keyctl show handle deeply nested keyrings [BZ 1075652].
- The key serial ID field displayed by keyctl show may be up to 10 digits [BZ 1075652].
- Make keyctl padd & co. handle binary data containing NUL chars [BZ 1075652].
- The input buffer for keyctl padd & co. should be 1MB-1 in size [BZ 1075652].

* Fri Feb 3 2012 David Howells  <dhowells@redhat.com> - 1.4-4
- Allow /sbin/request-key to have multiple config files [BZ 772497].

* Thu Aug 11 2011 David Howells  <dhowells@redhat.com> - 1.4-3
- Make the keyutils rpm depend on the same keyutils-libs rpm version [BZ 730002].

* Tue Aug 9 2011 David Howells  <dhowells@redhat.com> - 1.4-2
- Pass -Wl,-z,relro to the linker as a security enhancement [BZ 727280].

* Fri Mar 19 2010 David Howells  <dhowells@redhat.com> - 1.4-1
- Fix the library naming wrt the version.
- Move the package to version to 1.4.

* Fri Mar 19 2010 David Howells  <dhowells@redhat.com> - 1.3-3
- Fix spelling mistakes in manpages.
- Add an index manpage for all the keyctl functions.

* Thu Mar 11 2010 David Howells  <dhowells@redhat.com> - 1.3-2
- Fix rpmlint warnings.

* Fri Feb 26 2010 David Howells <dhowells@redhat.com> - 1.3-1
- Fix compiler warnings in request-key.
- Expose the kernel function to get a key's security context.
- Expose the kernel function to set a processes keyring onto its parent.
- Move libkeyutils library version to 1.3.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2-6.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Todd Zullinger <tmz@pobox.com> - 1.2-4
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-3
- Autorebuild for GCC 4.3

* Tue Aug 22 2006 David Howells <dhowells@redhat.com> - 1.2-1
- Remove syscall manual pages (section 2) to man-pages package [BZ 203582]
- Don't write to serial port in debugging script

* Mon Jun 5 2006 David Howells <dhowells@redhat.com> - 1.1-4
- Call ldconfig during (un)installation.

* Fri May 5 2006 David Howells <dhowells@redhat.com> - 1.1-3
- Don't include the release number in the shared library filename
- Don't build static library

* Fri May 5 2006 David Howells <dhowells@redhat.com> - 1.1-2
- More bug fixes from Fedora reviewer.

* Thu May 4 2006 David Howells <dhowells@redhat.com> - 1.1-1
- Fix rpmlint errors

* Mon Dec 5 2005 David Howells <dhowells@redhat.com> - 1.0-2
- Add build dependency on glibc-kernheaders with key management syscall numbers

* Tue Nov 29 2005 David Howells <dhowells@redhat.com> - 1.0-1
- Add data pipe-in facility for keyctl request2

* Mon Nov 28 2005 David Howells <dhowells@redhat.com> - 1.0-1
- Rename library and header file "keyutil" -> "keyutils" for consistency
- Fix shared library version naming to same way as glibc.
- Add versioning for shared library symbols
- Create new keyutils-libs package and install library and main symlink there
- Install base library symlink in /usr/lib and place in devel package
- Added a keyutils archive library
- Shorten displayed key permissions list to just those we actually have

* Thu Nov 24 2005 David Howells <dhowells@redhat.com> - 0.3-4
- Add data pipe-in facilities for keyctl add, update and instantiate

* Fri Nov 18 2005 David Howells <dhowells@redhat.com> - 0.3-3
- Added stdint.h inclusion in keyutils.h
- Made request-key.c use request_key() rather than keyctl_search()
- Added piping facility to request-key

* Thu Nov 17 2005 David Howells <dhowells@redhat.com> - 0.3-2
- Added timeout keyctl option
- request_key auth keys must now be assumed
- Fix keyctl argument ordering for debug negate line in request-key.conf

* Thu Jul 28 2005 David Howells <dhowells@redhat.com> - 0.3-1
- Must invoke initialisation from perror() override in libkeyutils
- Minor UI changes

* Wed Jul 20 2005 David Howells <dhowells@redhat.com> - 0.2-2
- Bump version to permit building in main repositories.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.2-1
- Don't attempt to define the error codes in the header file.
- Pass the release ID through to the makefile to affect the shared library name.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.1-3
- Build in the perror() override to get the key error strings displayed.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.1-2
- Need a defattr directive after each files directive.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.1-1
- Package creation.
