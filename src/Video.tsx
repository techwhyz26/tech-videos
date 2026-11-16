import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import type {SceneProps, SceneType, Spec} from './types';
import {resolveTimeline} from './timeline';
import {clamp, pickTheme} from './theme';
import {Background, Brand, Progress} from './components/Background';
import {Captions} from './components/Captions';
import {TitleScene} from './scenes/TitleScene';
import {CrowdScene} from './scenes/CrowdScene';
import {PillsScene} from './scenes/PillsScene';
import {HubScene} from './scenes/HubScene';
import {StepsScene} from './scenes/StepsScene';
import {StatScene} from './scenes/StatScene';
import {CompareScene} from './scenes/CompareScene';
import {IconScene} from './scenes/IconScene';
import {WordsScene} from './scenes/WordsScene';
import {ChartScene} from './scenes/ChartScene';
import {PhoneScene} from './scenes/PhoneScene';
import {CardScene} from './scenes/CardScene';
import {GridScene} from './scenes/GridScene';
import {ImageScene} from './scenes/ImageScene';
import {ArtScene} from './scenes/ArtScene';

const SCENES: Record<SceneType, React.FC<SceneProps>> = {
  title: TitleScene,
  crowd: CrowdScene,
  pills: PillsScene,
  hub: HubScene,
  steps: StepsScene,
  stat: StatScene,
  compare: CompareScene,
  icon: IconScene,
  words: WordsScene,
  chart: ChartScene,
  phone: PhoneScene,
  card: CardScene,
  grid: GridScene,
  image: ImageScene,
  art: ArtScene,
};

/** Entrance (rotates between fade, rise and zoom), slow camera push, and exit fade for one scene. */
const Shell: React.FC<{frames: number; index: number; children: React.ReactNode}> = ({
  frames,
  index,
  children,
}) => {
  const frame = useCurrentFrame();
  const out = Math.max(9, frames - 5);
  const opacity = frames < 16 ? 1 : interpolate(frame, [0, 6, out, frames], [0, 1, 1, 0], clamp);
  const enter = interpolate(frame, [0, 9], [1, 0], clamp);
  const push = 1 + (frame / Math.max(1, frames)) * 0.045;
  const mode = index % 3;
  const transform =
    mode === 1
      ? `translateY(${enter * 70}px) scale(${push})`
      : mode === 2
        ? `scale(${push * (1 - enter * 0.08)})`
        : `scale(${push})`;
  return <AbsoluteFill style={{opacity, transform}}>{children}</AbsoluteFill>;
};

export const Video: React.FC<Spec> = (spec) => {
  const timeline = resolveTimeline(spec);
  const theme = pickTheme(spec.theme, spec.slug);
  const vars = {
    '--body': theme.body,
    '--display': theme.display,
    '--bg': theme.bg,
    '--accent': theme.accent,
    '--accent2': theme.accent2,
  } as React.CSSProperties;

  return (
    <AbsoluteFill style={{...vars, fontFamily: theme.body, color: '#fff', backgroundColor: theme.bg}}>
      <Background theme={theme} />
      {timeline.map((s, i) => {
        const Comp = SCENES[s.type] ?? TitleScene;
        return (
          <Sequence key={i} from={s.from} durationInFrames={s.frames}>
            {/* An inverted scene flips to a light background while keeping its hues. */}
            <AbsoluteFill style={s.invert ? {filter: 'invert(1) hue-rotate(180deg)'} : undefined}>
              {s.invert ? <AbsoluteFill style={{backgroundColor: theme.bg}} /> : null}
              <Shell frames={s.frames} index={i}>
                <Comp props={s.props ?? {}} accent={theme.accent} frames={s.frames} />
              </Shell>
              <Captions words={s.words} emphasis={s.emphasis ?? []} accent={theme.accent} style={theme.caption} />
            </AbsoluteFill>
            {s.audio ? <Audio src={staticFile(s.audio)} /> : null}
          </Sequence>
        );
      })}
      {spec.brand?.name ? <Brand name={spec.brand.name} /> : null}
      <Progress accent={theme.accent} />
    </AbsoluteFill>
  );
};
