import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';

const Glow: React.FC<{theme: Theme}> = ({theme}) => {
  const frame = useCurrentFrame();
  const x = 50 + Math.sin(frame / 90) * 12;
  const y = 58 + Math.cos(frame / 120) * 6;
  return (
    <AbsoluteFill
      style={{background: `radial-gradient(900px 900px at ${x}% ${y}%, ${theme.accent}33, transparent 70%)`}}
    />
  );
};

const Grid: React.FC<{theme: Theme}> = ({theme}) => {
  const frame = useCurrentFrame();
  const line = `${theme.accent}1c`;
  return (
    <>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${line} 2px, transparent 2px), linear-gradient(90deg, ${line} 2px, transparent 2px)`,
          backgroundSize: '90px 90px',
          backgroundPosition: `0 ${(frame * 0.6) % 90}px`,
          maskImage: 'radial-gradient(900px 1100px at 50% 55%, #000 20%, transparent 85%)',
          WebkitMaskImage: 'radial-gradient(900px 1100px at 50% 55%, #000 20%, transparent 85%)',
        }}
      />
      <AbsoluteFill
        style={{background: `radial-gradient(700px 700px at 50% 60%, ${theme.accent}22, transparent 70%)`}}
      />
    </>
  );
};

const Beams: React.FC<{theme: Theme}> = ({theme}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            top: -300,
            left: -200 + i * 420 + Math.sin(frame / 70 + i) * 40,
            width: 260 - i * 40,
            height: 2400,
            transform: `rotate(${-24 + i * 3}deg)`,
            transformOrigin: 'top left',
            background: `linear-gradient(180deg, ${i === 1 ? theme.accent2 : theme.accent}38, transparent 70%)`,
            filter: 'blur(50px)',
          }}
        />
      ))}
    </>
  );
};

const Orbs: React.FC<{theme: Theme}> = ({theme}) => {
  const frame = useCurrentFrame();
  const orb = (color: string, size: number, x: number, y: number): React.CSSProperties => ({
    position: 'absolute',
    width: size,
    height: size,
    left: x - size / 2,
    top: y - size / 2,
    borderRadius: '50%',
    background: color,
    filter: 'blur(160px)',
    opacity: 0.32,
  });
  return (
    <>
      <div style={orb(theme.accent, 800, 250 + Math.sin(frame / 80) * 160, 600 + Math.cos(frame / 100) * 140)} />
      <div style={orb(theme.accent2, 620, 850 + Math.cos(frame / 90) * 140, 1350 + Math.sin(frame / 70) * 160)} />
    </>
  );
};

const BACKDROPS = {glow: Glow, grid: Grid, beams: Beams, orbs: Orbs};

export const Background: React.FC<{theme: Theme}> = ({theme}) => {
  const Backdrop = BACKDROPS[theme.backdrop];
  return (
    <AbsoluteFill style={{backgroundColor: theme.bg, overflow: 'hidden'}}>
      <Backdrop theme={theme} />
      <AbsoluteFill
        style={{
          background: 'radial-gradient(1400px 1700px at 50% 50%, transparent 55%, rgba(0,0,0,0.7) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};

export const Progress: React.FC<{accent: string}> = ({accent}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        height: 6,
        width: `${(frame / Math.max(1, durationInFrames - 1)) * 100}%`,
        background: accent,
      }}
    />
  );
};

export const Brand: React.FC<{name: string}> = ({name}) => (
  <div
    style={{
      position: 'absolute',
      top: 170,
      left: 0,
      right: 0,
      textAlign: 'center',
      fontSize: 28,
      fontWeight: 600,
      letterSpacing: 10,
      textTransform: 'uppercase',
      color: 'rgba(255,255,255,0.55)',
      mixBlendMode: 'difference',
    }}
  >
    {name}
  </div>
);
