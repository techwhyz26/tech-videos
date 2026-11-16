import {loadFont as loadPoppins} from '@remotion/google-fonts/Poppins';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadDMSans} from '@remotion/google-fonts/DMSans';
import {loadFont as loadSpaceGrotesk} from '@remotion/google-fonts/SpaceGrotesk';
import {loadFont as loadAnton} from '@remotion/google-fonts/Anton';
import {loadFont as loadBebas} from '@remotion/google-fonts/BebasNeue';
import {loadFont as loadOswald} from '@remotion/google-fonts/Oswald';
import {loadFont as loadBarlow} from '@remotion/google-fonts/BarlowCondensed';
import {spring} from 'remotion';

const text = {weights: ['500', '600', '700'] as any, subsets: ['latin'] as any};
const poppins = loadPoppins('normal', text).fontFamily;
const inter = loadInter('normal', text).fontFamily;
const dmSans = loadDMSans('normal', text).fontFamily;
const grotesk = loadSpaceGrotesk('normal', text).fontFamily;
const anton = loadAnton('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;
const bebas = loadBebas('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;
const oswald = loadOswald('normal', {weights: ['700'], subsets: ['latin']}).fontFamily;
const barlow = loadBarlow('normal', {weights: ['800'], subsets: ['latin']}).fontFamily;

export type Theme = {
  name: string;
  bg: string;
  accent: string;
  /** Second colour, used for the "active" state and warnings. */
  accent2: string;
  display: string;
  body: string;
  caption: 'pop' | 'box' | 'pill';
  backdrop: 'glow' | 'grid' | 'beams' | 'orbs';
};

export const THEMES: Theme[] = [
  {name: 'violet', bg: '#07070c', accent: '#8f7cff', accent2: '#ffc93c', display: anton, body: poppins, caption: 'pop', backdrop: 'glow'},
  {name: 'ember', bg: '#120c08', accent: '#ff8a3d', accent2: '#ffe08a', display: bebas, body: dmSans, caption: 'box', backdrop: 'beams'},
  {name: 'matrix', bg: '#040a07', accent: '#3dff8f', accent2: '#eaff6b', display: barlow, body: grotesk, caption: 'box', backdrop: 'grid'},
  {name: 'ocean', bg: '#05101c', accent: '#38c6ff', accent2: '#ff6b9a', display: oswald, body: inter, caption: 'pill', backdrop: 'orbs'},
  {name: 'gold', bg: '#0b0a08', accent: '#f5c451', accent2: '#ff7a59', display: anton, body: inter, caption: 'pill', backdrop: 'grid'},
  {name: 'crimson', bg: '#0d0507', accent: '#ff4d6d', accent2: '#ffd23f', display: bebas, body: poppins, caption: 'pop', backdrop: 'beams'},
];

/** Theme named in the spec, otherwise a stable pick based on the video's slug. */
export const pickTheme = (name: string | undefined, slug: string): Theme => {
  const named = THEMES.find((t) => t.name === name);
  if (named) return named;
  let h = 0;
  for (const c of slug) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return THEMES[h % THEMES.length];
};

// Scenes read fonts and shared colours through CSS variables that Video.tsx sets from the theme.
export const body = 'var(--body)';
export const display = 'var(--display)';
export const BG = 'var(--bg)';
export const AMBER = 'var(--accent2)';

/** 0 -> 1 spring that starts at `delay` frames. */
export const pop = (frame: number, fps: number, delay = 0, damping = 14) =>
  spring({frame: frame - delay, fps, config: {damping, stiffness: 150, mass: 0.8}});

export const clamp = {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
} as const;
