import React from 'react';
import {AbsoluteFill} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Poppins';

// Channel artwork: profile picture ("Logo", 1080x1080) and YouTube banner ("Banner", 2560x1440).
// Render with:  npx remotion still src/index.ts Logo output/brand/profile.png --props='{"palette":"sunset"}'

const {fontFamily} = loadFont('normal', {weights: ['600', '800'], subsets: ['latin']});

type Palette = {
  bg: string; // background, dark
  glow: string; // soft glow behind the mark
  q1: string; // question mark gradient start
  q2: string; // ... middle
  q3: string; // ... end
  chip: string; // the dot / chip
  trace: string; // circuit lines
  word: string; // "Whyz" in the wordmark
  tag: string; // small tagline
};

export const PALETTES: Record<string, Palette> = {
  sunset: {bg: '#170a1c', glow: '#3d1236', q1: '#ffd36e', q2: '#ff7a59', q3: '#ff3d77', chip: '#ffffff', trace: '#ff7a59', word: '#ff7a59', tag: '#ffd36e'},
  lime: {bg: '#0a0f0b', glow: '#16301c', q1: '#f4ffb0', q2: '#b6ff3b', q3: '#2ee59d', chip: '#ffffff', trace: '#7dffa9', word: '#b6ff3b', tag: '#2ee59d'},
  fire: {bg: '#120708', glow: '#3a0f10', q1: '#ffffff', q2: '#ff8a00', q3: '#ff2e2e', chip: '#ffd400', trace: '#ff5a36', word: '#ff4a2e', tag: '#ffd400'},
  bold: {bg: '#0e0e10', glow: '#26262b', q1: '#ffffff', q2: '#ffffff', q3: '#d9d9e0', chip: '#ffd400', trace: '#ffd400', word: '#ffd400', tag: '#ffffff'},
  candy: {bg: '#10071f', glow: '#2b1150', q1: '#7cf7ff', q2: '#ff6bd6', q3: '#ff3d8b', chip: '#ffe66d', trace: '#ff6bd6', word: '#ff6bd6', tag: '#7cf7ff'},
  mint: {bg: '#06141a', glow: '#0c3036', q1: '#ffffff', q2: '#5ff2c9', q3: '#13b8a6', chip: '#ff6b5e', trace: '#5ff2c9', word: '#5ff2c9', tag: '#ff8f84'},
};

type Props = {palette?: string};
const pick = (p?: string) => PALETTES[p ?? ''] ?? PALETTES.fire; // fire is the channel's chosen look

/** The mark: a "?" whose dot is a glowing chip with circuit traces. Drawn in a 1000x1000 box. */
const Mark: React.FC<{size: number; c: Palette}> = ({size, c}) => (
  <svg width={size} height={size} viewBox="0 0 1000 1000">
    <defs>
      <linearGradient id="q" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor={c.q1} />
        <stop offset="0.5" stopColor={c.q2} />
        <stop offset="1" stopColor={c.q3} />
      </linearGradient>
      <filter id="g" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="22" result="b" />
        <feMerge>
          <feMergeNode in="b" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
    <g fill="none" stroke={c.trace} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" opacity={0.9}>
      <path d="M430 820 H300 L240 760 H150" />
      <path d="M570 820 H700 L760 880 H850" />
      <path d="M500 890 V950" />
    </g>
    <g fill={c.trace}>
      <circle cx="150" cy="760" r="22" />
      <circle cx="850" cy="880" r="22" />
      <circle cx="500" cy="955" r="20" />
    </g>
    <path
      d="M300 330 C300 180 400 100 510 100 C640 100 720 190 720 300 C720 400 650 450 590 490 C540 523 520 555 520 620 V660"
      fill="none"
      stroke="url(#q)"
      strokeWidth={118}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <g filter="url(#g)">
      <rect x="430" y="750" width="140" height="140" rx="30" fill={c.chip} />
    </g>
    <rect x="462" y="782" width="76" height="76" rx="12" fill={c.bg} opacity={0.3} />
  </svg>
);

const Backdrop: React.FC<{c: Palette}> = ({c}) => (
  <AbsoluteFill style={{background: `radial-gradient(circle at 50% 42%, ${c.glow} 0%, ${c.bg} 62%)`}} />
);

export const Logo: React.FC<Props> = ({palette}) => {
  const c = pick(palette);
  return (
    <AbsoluteFill>
      <Backdrop c={c} />
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
        <Mark size={760} c={c} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Traces: React.FC<{c: Palette}> = ({c}) => {
  // faint circuit lines across the whole banner (TVs show all of it, phones only the middle)
  const lines = [];
  for (let i = 0; i < 14; i++) {
    const y = 80 + i * 100;
    const x = (i * 337) % 900;
    lines.push(
      <path key={i} d={`M${x} ${y} H${x + 380} L${x + 440} ${y + 60} H${x + 820}`}
        stroke={i % 3 === 0 ? c.q3 : c.trace} strokeWidth={4} fill="none" opacity={0.12} />,
      <circle key={`c${i}`} cx={x + 820} cy={y + 60} r={9} fill={c.trace} opacity={0.18} />,
    );
  }
  return (
    <svg width={2560} height={1440} viewBox="0 0 2560 1440" style={{position: 'absolute'}}>
      <g>{lines}</g>
      <g transform="translate(2560 0) scale(-1 1)">{lines}</g>
    </svg>
  );
};

export const Banner: React.FC<Props> = ({palette}) => {
  const c = pick(palette);
  return (
    <AbsoluteFill>
      <Backdrop c={c} />
      <Traces c={c} />
      {/* everything important sits inside YouTube's 1546x423 safe area in the middle */}
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 50}}>
          <Mark size={380} c={c} />
          <div style={{fontFamily, color: '#fff'}}>
            <div style={{fontSize: 190, fontWeight: 800, letterSpacing: -4, lineHeight: 1}}>
              Tech<span style={{color: c.word}}>Whyz</span>
            </div>
            <div style={{fontSize: 54, fontWeight: 600, opacity: 0.85, marginTop: 22}}>
              How everyday tech actually works
            </div>
            <div style={{fontSize: 40, fontWeight: 600, color: c.tag, marginTop: 14}}>New videos every day</div>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
