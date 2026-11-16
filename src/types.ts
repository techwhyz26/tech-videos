export type Word = {text: string; startMs: number; endMs: number};

export type SceneType =
  | 'title'
  | 'crowd'
  | 'pills'
  | 'hub'
  | 'steps'
  | 'stat'
  | 'compare'
  | 'icon'
  | 'words'
  | 'chart'
  | 'phone'
  | 'card'
  | 'grid'
  | 'image'
  | 'art';

export type Scene = {
  type: SceneType;
  /** What the voice says during this scene. */
  narration: string;
  /** Words from the narration to highlight in the captions. */
  emphasis?: string[];
  /** Scene-specific visual settings, see README. */
  props?: Record<string, any>;
  /** Show this scene on a light background for contrast. */
  invert?: boolean;
  /** Filled in by the voice step. */
  audio?: string;
  durationMs?: number;
  words?: Word[];
};

export type Spec = {
  slug: string;
  title: string;
  /** One of the theme names in theme.ts; picked automatically from the slug when omitted. */
  theme?: string;
  brand?: {name?: string};
  caption?: string;
  scenes: Scene[];
};

export type SceneProps = {
  props: Record<string, any>;
  accent: string;
  /** Length of this scene in frames. */
  frames: number;
};
