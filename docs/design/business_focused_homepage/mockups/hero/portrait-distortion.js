(() => {
  const frame = document.querySelector("[data-distortion-frame]");

  if (!frame) return;

  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let latestPointerEvent = null;
  let animationFrame = 0;

  const isEnabled = () => finePointer.matches && !reducedMotion.matches;

  const resetDistortion = () => {
    frame.classList.remove("is-distorting");
    frame.style.setProperty("--distort-x", "0px");
    frame.style.setProperty("--distort-y", "0px");
    frame.style.setProperty("--distort-skew", "0deg");
    frame.style.setProperty("--distort-hue", "0deg");
  };

  const renderDistortion = () => {
    animationFrame = 0;

    if (!latestPointerEvent || !isEnabled()) {
      resetDistortion();
      return;
    }

    const bounds = frame.getBoundingClientRect();
    const x = Math.max(0, Math.min(latestPointerEvent.clientX - bounds.left, bounds.width));
    const y = Math.max(0, Math.min(latestPointerEvent.clientY - bounds.top, bounds.height));
    const normalizedX = x / bounds.width - 0.5;
    const normalizedY = y / bounds.height - 0.5;

    frame.style.setProperty("--lens-x", `${x}px`);
    frame.style.setProperty("--lens-y", `${y}px`);
    frame.style.setProperty("--distort-x", `${normalizedX * 18}px`);
    frame.style.setProperty("--distort-y", `${normalizedY * 12}px`);
    frame.style.setProperty("--distort-skew", `${normalizedX * -3}deg`);
    frame.style.setProperty("--distort-hue", `${normalizedX * 10}deg`);
    frame.classList.add("is-distorting");
  };

  frame.addEventListener("pointermove", (event) => {
    if (!isEnabled()) return;
    latestPointerEvent = event;

    if (!animationFrame) {
      animationFrame = window.requestAnimationFrame(renderDistortion);
    }
  });

  frame.addEventListener("pointerleave", () => {
    latestPointerEvent = null;
    resetDistortion();
  });

  finePointer.addEventListener("change", resetDistortion);
  reducedMotion.addEventListener("change", resetDistortion);
})();
