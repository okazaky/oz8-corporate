import ja from './ja.json';
import en from './en.json';

export const translations = {
  ja,
  en
} as const;

export type Locale = keyof typeof translations;

export function getTranslations(locale: Locale) {
  return translations[locale];
}

export function getCurrentLocale(pathname: string): Locale {
  if (pathname.startsWith('/en')) {
    return 'en';
  }
  return 'ja';
}

export function getAlternateUrl(currentPath: string, targetLocale: Locale): string {
  const isEnglish = currentPath.startsWith('/en');

  if (targetLocale === 'en' && !isEnglish) {
    return `/en${currentPath}`;
  }

  if (targetLocale === 'ja' && isEnglish) {
    return currentPath.replace('/en', '') || '/';
  }

  return currentPath;
}
