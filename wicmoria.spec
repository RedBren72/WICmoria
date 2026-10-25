%global debug_package %{nil}

%if 0%{?suse_version} || 0%{?rhel} == 8
%define __builddir %{_vpath_builddir}
%endif

Name:           wicmoria
Version:        0.2.2
Release:        1%{?dist}
Summary:    	wicmoria %{version}

License:        GPL-3.0
URL:            https://umoria.org 
Source0:        wicmoria-%{version}.tar.gz

BuildRequires:  ncurses-devel gcc-c++ cmake
Requires:       ncurses-libs


%description
The Dungeons of Moria is a single player dungeon simulation originally written by Robert Alan Koeneke, with its first public release in 1983.
The game was originally developed using VMS Pascal before being ported to the C language by James E. Wilson in 1988, and released a Umoria.
WICmoria is a fork of Umoria 5.17.15 that repurposes INT and WIS to determine mana and spell slots respectively.

%prep
%autosetup

%build

%if 0%{?rhel} == 8
mkdir %{_vpath_builddir} && (cd %{_vpath_builddir}; %cmake ..; %cmake_build )
%else
%cmake
%cmake_build
%endif


%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp %{_vpath_builddir}/WICmoria/wicmoria $RPM_BUILD_ROOT/%{_bindir}/wicmoria.bin
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/games/wicmoria
cp -R %{_vpath_builddir}/WICmoria/data $RPM_BUILD_ROOT/%{_datadir}/games/wicmoria
cp LICENSE $RPM_BUILD_ROOT/%{_datadir}/games/wicmoria/data/LICENSE
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/wicmoria/historical
cp historical/* $RPM_BUILD_ROOT/%{_docdir}/wicmoria/historical

cat << EOF > $RPM_BUILD_ROOT/%{_bindir}/wicmoria
#!/bin/sh
CONFDIR=~/.config/wicmoria
DATADIR=%{_datadir}/games/wicmoria/data
BIN=%{_bindir}/wicmoria.bin
[ ! -d \$CONFDIR ] && mkdir -p \$CONFDIR && ln -s \$DATADIR \$CONFDIR/data
[ ! -e \$CONFDIR/LICENSE ] && ln -s \$DATADIR/LICENSE \$CONFDIR/LICENSE
[ ! -f \$CONFDIR/scores.dat ] && touch \$CONFDIR/scores.dat
(cd \$CONFDIR; \$BIN \$@)
EOF

chmod +x $RPM_BUILD_ROOT/%{_bindir}/wicmoria

%postun
echo "Please remove each user's ~/.config/wicmoria manually, if you need."

%files
%{_bindir}/wicmoria*
%{_datadir}/games/wicmoria/data/*
%{_docdir}/wicmoria/historical/*
%license LICENSE
%doc *.md

%changelog
* Sun Oct 25 2026 Brendan Weir <brendanweir13@gmail.com> - 0.2.2
- Fixed a bug where players forgetting spells is treated the same as amnesia,
  leading to the forgotten spell being auto-remembered when the player is next
  able to learn a spell.

* Tue Oct 20 2026 Brendan Weir <brendanweir13@gmail.com> - 0.2.1
- Updated the README.md file.

* Mon Oct 19 2026 Brendan Weir <brendanweir13@gmail.com> - 0.2.0
- To compensate for the lower number of spell slots that arcane magic users
  now have due to their lower WIS, they can now forget learned spells and
  learn new ones, but only in town - just like prior to a D&D campaign.
- Priests cannot forget the prayers revealed to them by their deities.
- Paladins can forget prayers as they are followers not conduits of faith.


* Sat Oct 10 2026 Brendan Weir <brendanweir13@gmail.com> - 0.1.0
- This is a fork from umoria that makes INT and WIS from being class-specific
  duplicates to having distinct purposes.

