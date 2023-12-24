// Date format utilities

import { format } from "date-fns";
import { enUS } from "date-fns/locale/en-US";

const postPattern = "eeee, dd MMM yyyy";

export function rfc2822(date) {
  const pattern = "eee, dd MMM yyyy HH:mm:ss zzz";

  return format(date, pattern, { locale: enUS });
}

export function postdate(date) {
  return format(date, postPattern, { locale: enUS });
}

export function year() {
  return format(new Date(), "yyyy");
}
