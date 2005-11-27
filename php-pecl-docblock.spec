%define		_modname	docblock
%define		_status		alpha
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - phpDocumentor-style DocBlock tokenizer
Summary(pl):	%{_modname} - tokenizer DocBlock podobny do phpDocumentora
Name:		php-pecl-%{_modname}
Version:	0.1.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	1f1566badd670a3d2f095e2a9647f290
URL:		http://pecl.php.net/package/docblock/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
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

In PECL status of this extension is: %{_status}.

%description -l pl
Rozszerzenie to jest odpowienikiem rozszerzenia tokenizer. Przyjmuje
blok komentarza podobny do:

/**
 - information {@inlinetag}
 - @tags
 - */

i przetwarza go w tokeny.

Podstawow± funkcj± jest docblock_tokenize(), która jako argument
przyjmuje string, a zwraca tablicê tablic (TOKEN, "token"). TOKEN to
jedna ze sta³ych DOCBLOCK_*.

docblock_tokenize() mo¿e tak¿e przyj±æ opcjonalnie drugi argument
(typu boolean), która okresla czy funkcja ma wypisaæ nieistotne tokeny
takie jak /** * (znaczniki komentarza).

docblock_token_name() jako argument przyjmuje sta³± DOCBLOCK_* i
zwraca jej nazwê.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL,tests}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
