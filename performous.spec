Summary:	Performous - a free cross-platform singing game
Name:		performous
Version:	0.6.1
Release:	3
License:	GPL v2+
Group:		Applications
Source0:	http://downloads.sourceforge.net/performous/Performous-%{version}-Source.tar.bz2
# Source0-md5:	451a759de77984b5a699e91107fe52e2
URL:		http://performous.org/
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
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
BuildRequires:	pulseaudio-devel
Suggests:	%{name}-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
While Performous might be classified as a karaoke program, it is
actually much more than that. Instead of just displaying the lyrics,
notes are also displayed and the performance is scored based on how
well you actually hit the notes. Unlike in most other games in this
genre, you will also see the precise pitch that you are singing, so
that you can see what you are doing wrong and easily (well, everything
is relative) correct your pitch.

Most of the songs available also contain the original vocals and
actual karaoke versions are rare.

For those who sing rather than well, a karaoke mode is provided. In
this mode only lyrics are displayed and there are no notes or scoring.

%package tools
Summary:	Performous tools
Group:		Applications

%description tools
Provides several utilities for converting data files for Performous.

%prep
%setup -qn Performous-%{version}-Source
%{__sed} -i 's:png12:png14:g' cmake/Modules/FindPng.cmake

%build
mkdir build
cd build
%cmake .. \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
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

install docs/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/*.txt
%attr(755,root,root) %{_bindir}/performous
%{_datadir}/games/%{name}
%{_mandir}/man6/*
%{_pixmapsdir}/*
%{_desktopdir}/*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gh_*
%attr(755,root,root) %{_bindir}/itg_pck
%attr(755,root,root) %{_bindir}/ss_*
%{_mandir}/man1/*
