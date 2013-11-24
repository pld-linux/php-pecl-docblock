%define		php_name	php%{?php_suffix}
%define		modname	docblock
%define		status		alpha
Summary:	%{modname} - phpDocumentor-style DocBlock tokenizer
Summary(pl.UTF-8):	%{modname} - tokenizer DocBlock podobny do phpDocumentora
Name:		%{php_name}-pecl-%{modname}
Version:	0.2.0
Release:	4
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	678a888b8110a3d31ddcedd03d93bb0c
URL:		http://pecl.php.net/package/docblock/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension is like the tokenizer extension for PHP. It takes a
document comment (docblock) like this one:

/**
 - information {@inlinetag}
 - @tags
 - */

and parses it into tokens.

The primary function is docblock_tokenize(), which accepts a string,
and returns an array of arrays of array(TOKEN, "token"). TOKEN is one
of DOCBLOCK_* constants.

docblock_tokenize() has an optional second bool parameter that
determine whether to output non-essential tokens like the /** * stuff.

docblock_token_name() takes a DOCBLOCK_* constant and returns its name

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to jest odpowienikiem rozszerzenia tokenizer. Przyjmuje
blok komentarza podobny do:

/**
 - information {@inlinetag}
 - @tags
 - */

i przetwarza go w tokeny.

Podstawową funkcją jest docblock_tokenize(), która jako argument
przyjmuje string, a zwraca tablicę tablic (TOKEN, "token"). TOKEN to
jedna ze stałych DOCBLOCK_*.

docblock_tokenize() może także przyjąć opcjonalnie drugi argument
(typu boolean), która okresla czy funkcja ma wypisać nieistotne tokeny
takie jak /** * (znaczniki komentarza).

docblock_token_name() jako argument przyjmuje stałą DOCBLOCK_* i
zwraca jej nazwę.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL tests
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
