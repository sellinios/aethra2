declare module 'skycons' {
  export default class Skycons {
    constructor(options?: { color?: string });
    add(element: HTMLElement | string, type: string): void;
    set(element: HTMLElement | string, type: string): void;
    remove(element: HTMLElement | string): void;
    play(): void;
    pause(): void;
  }
}