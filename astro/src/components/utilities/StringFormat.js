// String formatting functions

export function camelize(str) {
  return str
    .toLowerCase()
    .replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase());
}

export function titleCase(str) {
  //  return str.replace(/\b[A-Za-z]/g, (x) => x.toUpperCase());

  var smallWords =
    /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/i;

  return str.replace(
    /[A-Za-z0-9\u00C0-\u00FF]+[^\s-]*/g,
    function (match, index, title) {
      if (
        index > 0 &&
        index + match.length !== title.length &&
        match.search(smallWords) > -1 &&
        title.charAt(index - 2) !== ":" &&
        (title.charAt(index + match.length) !== "-" ||
          title.charAt(index - 1) === "-") &&
        title.charAt(index - 1).search(/[^\s-]/) < 0
      ) {
        return match.toLowerCase();
      }
      if (match.substr(1).search(/[A-Z]|\../) > -1) {
        return match;
      }
      return match.charAt(0).toUpperCase() + match.substr(1);
    }
  );
}

export function globalImageUrls(baseUrl, str) {
  let regex =
    /src="\/_astro\/([^"]+\.(?:jpg|jpeg|gif|png|webp|avif))"/g;
  // replace all image urls with the correct path
  return str
    .replaceAll(regex, 'src="' + baseUrl + '/_astro/$1"')
    .replaceAll("//_astro", "/_astro");
}

export function slugify(str) {
  return str
    .toString()
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^\w-]+/g, '')
    .replace(/--+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
}

export function deslugify(str) {
  return titleCase(str.replaceAll("-", " "));
}
