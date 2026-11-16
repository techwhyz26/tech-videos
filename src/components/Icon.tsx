import React from 'react';
import {display} from '../theme';

const P = (d: string) => <path d={d} />;

const ICONS: Record<string, React.ReactNode> = {
  lock: (
    <>
      <rect x="5" y="11" width="14" height="10" rx="2" />
      {P('M8 11V7a4 4 0 0 1 8 0v4')}
    </>
  ),
  key: (
    <>
      <circle cx="8" cy="15" r="4" />
      {P('M11 12l9-9M16 7l3 3M13.5 9.5l2 2')}
    </>
  ),
  play: P('M7 4l13 8-13 8z'),
  download: P('M12 3v12M7 10l5 5 5-5M4 20h16'),
  upload: P('M12 16V4M7 9l5-5 5 5M4 20h16'),
  chip: (
    <>
      <rect x="7" y="7" width="10" height="10" rx="1.5" />
      {P('M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4')}
    </>
  ),
  globe: (
    <>
      <circle cx="12" cy="12" r="9" />
      {P('M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18')}
    </>
  ),
  bolt: P('M13 2L5 14h6l-1 8 8-12h-6z'),
  cloud: P('M7 18a4 4 0 0 1-.5-7.97A6 6 0 0 1 18 9.5 4.25 4.25 0 0 1 17.5 18z'),
  server: (
    <>
      <rect x="4" y="4" width="16" height="6" rx="1.5" />
      <rect x="4" y="14" width="16" height="6" rx="1.5" />
      {P('M8 7h.01M8 17h.01')}
    </>
  ),
  phone: (
    <>
      <rect x="7" y="2" width="10" height="20" rx="2.5" />
      {P('M11 18h2')}
    </>
  ),
  shield: P('M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z'),
  coin: (
    <>
      <circle cx="12" cy="12" r="9" />
      {P('M12 6.5v11M15 9.5c0-1.2-1.3-2-3-2s-3 .8-3 2 1.3 1.9 3 2.4 3 1.2 3 2.6-1.3 2-3 2-3-.8-3-2')}
    </>
  ),
  wifi: P('M2 9a15 15 0 0 1 20 0M5.5 12.5a10 10 0 0 1 13 0M9 16a5 5 0 0 1 6 0M12 19.5h.01'),
  battery: (
    <>
      <rect x="2" y="8" width="17" height="8" rx="2" />
      {P('M22 11v2M6 11v2M9.5 11v2')}
    </>
  ),
  warning: P('M12 3l10 18H2zM12 10v5M12 18h.01'),
  check: P('M4 12.5l5 5L20 6.5'),
  code: P('M8 6l-6 6 6 6M16 6l6 6-6 6M14 4l-4 16'),
  user: (
    <>
      <circle cx="12" cy="8" r="4" />
      {P('M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7')}
    </>
  ),
  database: (
    <>
      <ellipse cx="12" cy="6" rx="8" ry="3" />
      {P('M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3')}
    </>
  ),
  gamepad: (
    <>
      <rect x="2" y="7" width="20" height="10" rx="5" />
      {P('M7 10v4M5 12h4M15.5 11h.01M18 13h.01')}
    </>
  ),
  eye: (
    <>
      {P('M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z')}
      <circle cx="12" cy="12" r="3" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="7" />
      {P('M16.5 16.5L21 21')}
    </>
  ),
  chart: P('M4 20V4M4 20h16M8 16v-4M12 16V8M16 16v-7'),
  robot: (
    <>
      <rect x="5" y="8" width="14" height="11" rx="2.5" />
      {P('M12 4.5V8M9 13h.01M15 13h.01M9.5 16h5M2 12v3M22 12v3')}
      <circle cx="12" cy="3.5" r="1" />
    </>
  ),
  factory: P('M3 21V10l6 4v-4l6 4V5h6v16zM7 17h2M12 17h2M17 17h2'),
  clock: (
    <>
      <circle cx="12" cy="12" r="9" />
      {P('M12 7v5l3.5 2')}
    </>
  ),
};

export const ICON_NAMES = Object.keys(ICONS);

/** Named line icon. Unknown names are drawn as text, so an emoji or a short word also works. */
export const Icon: React.FC<{name: string; size: number; color?: string; stroke?: number}> = ({
  name,
  size,
  color = '#fff',
  stroke = 1.6,
}) => {
  const icon = ICONS[name];
  if (!icon) {
    return (
      <div
        style={{
          width: size,
          height: size,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: display,
          fontSize: size * (name.length > 2 ? 0.42 : 0.8),
          color,
          lineHeight: 1,
        }}
      >
        {name}
      </div>
    );
  }
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      style={{stroke: color}}
      strokeWidth={stroke}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {icon}
    </svg>
  );
};
