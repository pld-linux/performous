#
# TODO:
#	- update Polish description, current is outdated (it is not only a
#	karaoke game any more)
Summary:	Performous - The All-in-One Music Game
Summary(pl.UTF-8):	Performous - wiele gier muzycznych w jednej
Name:		performous
Version:	0.6.1
Release:	18
License:	GPL v2+
Group:		Applications
Source0:	http://downloads.sourceforge.net/performous/Performous-%{version}-Source.tar.bz2
# Source0-md5:	451a759de77984b5a699e91107fe52e2
Patch0:		%{name}-ffmpeg.patch
Patch1:		%{name}-libpng15.patch
URL:		http://performous.org/
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	glew-devel
BuildRequires:	glibmm-devel
BuildRequires:	help2man
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libsigc++-devel
BuildRequires:	libxml++-devel
BuildRequires:	opencv-devel
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
Suggests:	%{name}-tools = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An open-source karaoke, band and dancing game where one or more
players perform a song and the game scores their perform ances.
Supports songs in UltraStar, Frets on Fire and StepMania formats.
Microphones and instruments from SingStar, Guit ar Hero and Rock Band
as well as some dance pads are autodetected.

%description -l pl.UTF-8
O ile Performous można zaklasyfikować jako program do karaoke, to jest
czymś o wiele więcej. Zamiast tylko wyświetlać tekst, wyświetlane są
także nuty, a wykonanie jest oceniane w oparciu o to, jak dobrze
pasuje do nut. W przeciwieństwie do innych gier tego gatunku podawana
jest także dokładna wysokość śpiewanych tonów, więc można zobaczyć, co
wykonuje się źle i (względnie) łatwo się poprawić.

Większość dostępnych piosenek zawiera także oryginalne wokale, zaś
wersje karaoke są dość rzadkie.

Dla śpiewających niezbyt dobrze dostępny jest tryb karaoke. W tyb
trybie wyświetlane są tylko słowa i nie ma nut ani oceniania.

%package tools
Summary:	Performous tools
Summary(pl.UTF-8):	Narzędzia do programu Performous
Group:		Applications

%description tools
Several utilities for converting data files for Performous.

%description tools -l pl.UTF-8
Zestaw narzędzi do konwersji danych dla programu Performous.

%prep
%setup -qn Performous-%{version}-Source
%patch0 -p1
%patch1 -p1
mkdir build

%build
cd build
%cmake .. \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
	-DCMAKE_CXX_FLAGS_RELEASE="%{rpmcxxflags} -DBOOST_FILESYSTEM_VERSION=2" \
	-DCMAKE_DEBUG_FLAGS_RELEASE="%{debugcflags} -DBOOST_FILESYSTEM_VERSION=2" \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install docs/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/{Authors,TODO,instruments}.txt
%attr(755,root,root) %{_bindir}/performous
%{_datadir}/games/%{name}
%{_mandir}/man6/performous.6*
%{_desktopdir}/performous.desktop
%{_pixmapsdir}/performous.xpm

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gh_*_decrypt
%attr(755,root,root) %{_bindir}/itg_pck
%attr(755,root,root) %{_bindir}/ss_*
%{_mandir}/man1/gh_*_decrypt.1*
%{_mandir}/man1/ss_*.1*
