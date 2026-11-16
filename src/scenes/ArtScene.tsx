import React, {useLayoutEffect, useRef} from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';

// Classes every illustration can use so it follows the video's theme.
const STYLE = `<style>
  .fa{fill:var(--accent)} .sa{stroke:var(--accent)}
  .fa2{fill:var(--accent2)} .sa2{stroke:var(--accent2)}
  .fb{fill:var(--bg)} .sb{stroke:var(--bg)}
  .fw{fill:#fff} .sw{stroke:#fff}
  .nf{fill:none}
  text{font-family:var(--body);font-weight:600;fill:#fff}
  .display{font-family:var(--display);font-weight:400}
</style>
<defs>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a56"/><stop offset="1" stop-color="#1e1e25"/></linearGradient>
<linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f4f8"/><stop offset="1" stop-color="#b9b9c6"/></linearGradient>
<linearGradient id="screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b1b24"/><stop offset="1" stop-color="#050507"/></linearGradient>
<linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9e5da"/></linearGradient>
</defs>`;
// The <defs> above are shared by every drawing (url(#metal), url(#soft), ...). Files made with
// tools/artlib.py carry an identical copy, which is harmless.

/**
 * props: { svg: string } - a custom illustration drawn for this exact sentence.
 * `svg` is the inner markup of a 1000x1000 SVG, animated with SMIL (<animate>, <animateTransform>,
 * <animateMotion>). The SVG clock is driven from the video frame, so every render is frame-accurate.
 * In a spec you normally write props.art = "name" and keep the drawing in art/name.svg next to it.
 */
export const ArtScene: React.FC<SceneProps> = ({props}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ref = useRef<SVGSVGElement>(null);

  useLayoutEffect(() => {
    const svg = ref.current;
    if (!svg) return;
    svg.pauseAnimations();
    svg.setCurrentTime(frame / fps);
  }, [frame, fps]);

  return (
    <AbsoluteFill>
      <svg
        ref={ref}
        viewBox="0 0 1000 1000"
        style={{position: 'absolute', left: 40, top: 520, width: 1000, height: 1000, overflow: 'visible'}}
        dangerouslySetInnerHTML={{__html: STYLE + String(props.svg ?? '')}}
      />
    </AbsoluteFill>
  );
};
