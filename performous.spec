Summary:	Performous - a free cross-platform singing game
Name:		performous
Version:	0.4.0
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://dl.sourceforge.net/performous/Performous-%{version}-Source.tar.bz2
# Source0-md5:	d7eafad29a94e3099c849d3c7208bfac
URL:		http://performous.org/
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	glew-devel
BuildRequires:	glibmm-devel
BuildRequires:	help2man
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	librsvg-devel
BuildRequires:	libsigc++-devel
BuildRequires:	libxml++-devel
BuildRequires:	pango-devel
BuildRequires:	pulseaudio-devel
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

%prep
%setup -qn Performous-%{version}-Source

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

cd ..


%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*.txt
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/libda-1
%attr(755,root,root) %{_libdir}/%{name}/libda-1/*.so
%{_datadir}/games/%{name}
%{_mandir}/man6/*
%{_pixmapsdir}/*
%{_desktopdir}/*
