
# TODO:
#	- consider init script / systemd job (uid/gid celery 274 used to be used)
#	  NOTE: this must not be included and enabled by default in the default
#	  package! Real-life deployments will mostly be application-specific.

# Conditional build:
%bcond_with	doc		# do build doc (too much dependencies to be worth the trouble)
%bcond_with	tests		# run tests (broken)

%define 	module	celery
Summary:	Celery - Distributed Task Query
Name:		python3-%{module}
Version:	5.0.5
Release:	1
License:	BSD-like
Group:		Development/Languages/Python
# Source0:	https://files.pythonhosted.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
Source0:	https://pypi.debian.net/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	a8193028841349fbc7c88e3b67ce608c
Source1:	amqp-objects.inv
Source2:	cyme-objects.inv
Source3:	djcelery-objects.inv
Source4:	kombu-objects.inv
Source5:	python-objects.inv
Patch0:		pytz_dependency.patch
URL:		http://celeryproject.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	sed >= 4.0
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
%endif
%if %{with doc}
BuildRequires:	python3-billiard
BuildRequires:	python3-django
BuildRequires:	python3-kombu
BuildRequires:	python3-pytz
BuildRequires:	python3-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-billiard >= 3.5.0.2
Requires:	python-kombu >= 4.2.0
Requires:	python-pytz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%package -n celery
Summary:	Celery - Distributed Task Query
Group:		Development/Languages/Python
Requires:	python3-%{module} = %{version}

%description -n celery
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%patch0 -p1

cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} docs

%build
%py3_build %{?with_tests:test}

%if %{with doc} && 0
cd docs
PYTHONPATH=../build-3/lib %{__make} -j1 html SPHINXBUILD=sphinx-build-3
rm -rf .build/html/_sources
mv .build .build3
cd ..
%endif

%install
%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build2/html/*
%endif

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt LICENSE README.rst TODO extra
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/celery-*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%files -n celery
%attr(755,root,root) %{_bindir}/*
