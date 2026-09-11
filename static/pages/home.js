(() => {
    const menu = document.querySelector("[data-home-mobile-nav]");
    if (!menu) return;

    const summary = menu.querySelector("summary");
    const links = menu.querySelectorAll("nav a");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let closeTimer;

    const updateLabel = (isOpen) => {
        summary.setAttribute("aria-expanded", String(isOpen));
        summary.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
    };

    const openMenu = () => {
        window.clearTimeout(closeTimer);
        menu.classList.remove("is-closing");
        menu.open = true;
        updateLabel(true);

        window.requestAnimationFrame(() => {
            window.requestAnimationFrame(() => menu.classList.add("is-open"));
        });
    };

    const closeMenu = ({ returnFocus = false } = {}) => {
        if (!menu.open) return;

        window.clearTimeout(closeTimer);
        menu.classList.remove("is-open");
        menu.classList.add("is-closing");
        updateLabel(false);

        closeTimer = window.setTimeout(() => {
            menu.open = false;
            menu.classList.remove("is-closing");
            if (returnFocus) summary.focus();
        }, reducedMotion.matches ? 0 : 270);
    };

    menu.classList.add("is-ready");
    updateLabel(menu.open);
    if (menu.open) menu.classList.add("is-open");

    summary.addEventListener("click", (event) => {
        event.preventDefault();
        if (menu.open && !menu.classList.contains("is-closing")) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    links.forEach((link) => link.addEventListener("click", () => closeMenu()));

    document.addEventListener("pointerdown", (event) => {
        if (menu.open && !menu.contains(event.target)) closeMenu();
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && menu.open) closeMenu({ returnFocus: true });
    });
})();

(() => {
    const word = document.querySelector(".home-pixel-word");
    const canvas = word?.querySelector(".home-pixel-word-canvas");
    const text = word?.dataset.text;
    const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (!word || !canvas || !text || reducedMotion.matches) return;

    const context = canvas.getContext("2d");
    if (!context) return;

    const homePage = document.querySelector(".home-page");
    const rootStyle = getComputedStyle(homePage || document.documentElement);
    const colors = [
        rootStyle.getPropertyValue("--peach").trim() || "#f29576",
        rootStyle.getPropertyValue("--cream").trim() || "#f9e9d5",
    ];
    let particles = [];
    let pointer = { x: 0, y: 0 };
    let active = false;
    let revealed = false;
    let running = false;
    let revealTimer;
    let logicalWidth = 0;
    let logicalHeight = 0;

    const draw = () => {
        context.clearRect(0, 0, logicalWidth, logicalHeight);
        particles.forEach((particle) => {
            context.beginPath();
            context.fillStyle = particle.color;
            context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            context.fill();
        });
    };

    const buildParticles = () => {
        const bounds = word.getBoundingClientRect();
        const style = getComputedStyle(word);
        const fontSize = parseFloat(style.fontSize);
        const padding = Math.max(24, Math.round(fontSize * 0.48));
        const wordWidth = Math.ceil(bounds.width);
        const wordHeight = Math.ceil(bounds.height);
        const ratio = Math.min(window.devicePixelRatio || 1, 2);
        const sample = document.createElement("canvas");
        const sampleContext = sample.getContext("2d", { willReadFrequently: true });

        if (!sampleContext || !wordWidth || !wordHeight) return;

        logicalWidth = wordWidth + padding * 2;
        logicalHeight = wordHeight + padding * 2;
        canvas.width = Math.ceil(logicalWidth * ratio);
        canvas.height = Math.ceil(logicalHeight * ratio);
        canvas.style.left = `${-padding}px`;
        canvas.style.top = `${-padding}px`;
        canvas.style.width = `${logicalWidth}px`;
        canvas.style.height = `${logicalHeight}px`;
        context.setTransform(ratio, 0, 0, ratio, 0, 0);

        sample.width = wordWidth;
        sample.height = wordHeight;
        sampleContext.fillStyle = "#fff";
        sampleContext.font = `${style.fontWeight} ${fontSize}px ${style.fontFamily}`;
        sampleContext.textBaseline = "alphabetic";

        const metrics = sampleContext.measureText(text);
        const ascent = metrics.actualBoundingBoxAscent || fontSize * 0.76;
        const descent = metrics.actualBoundingBoxDescent || fontSize * 0.2;
        const baseline = (wordHeight + ascent - descent) / 2;
        const scaleX = Math.min(1, wordWidth / Math.max(metrics.width, 1));
        sampleContext.save();
        sampleContext.scale(scaleX, 1);
        sampleContext.fillText(text, 0, baseline);
        sampleContext.restore();

        const pixels = sampleContext.getImageData(0, 0, wordWidth, wordHeight).data;
        const step = Math.max(4, Math.round(fontSize / 13));
        const nextParticles = [];

        for (let y = 0; y < wordHeight; y += step) {
            for (let x = 0; x < wordWidth; x += step) {
                if (pixels[(y * wordWidth + x) * 4 + 3] < 90) continue;
                const index = nextParticles.length;
                nextParticles.push({
                    baseX: padding + x,
                    baseY: padding + y,
                    color: colors[index % 9 === 0 ? 1 : 0],
                    radius: index % 5 === 0 ? step * 0.34 : step * 0.27,
                    vx: 0,
                    vy: 0,
                    x: padding + x,
                    y: padding + y,
                });
            }
        }

        particles = nextParticles;
        pointer = { x: logicalWidth / 2, y: logicalHeight / 2 };
        draw();
    };

    const animate = () => {
        const radius = Math.max(48, parseFloat(getComputedStyle(word).fontSize) * 0.82);
        const displacement = radius * 0.48;
        let settled = true;

        particles.forEach((particle) => {
            let targetX = particle.baseX;
            let targetY = particle.baseY;

            if (active) {
                const dx = particle.x - pointer.x;
                const dy = particle.y - pointer.y;
                const distance = Math.max(Math.hypot(dx, dy), 0.01);
                if (distance < radius) {
                    const force = (1 - distance / radius) * displacement;
                    targetX += (dx / distance) * force;
                    targetY += (dy / distance) * force;
                }
            }

            particle.vx = (particle.vx + (targetX - particle.x) * 0.16) * 0.7;
            particle.vy = (particle.vy + (targetY - particle.y) * 0.16) * 0.7;
            particle.x += particle.vx;
            particle.y += particle.vy;

            if (
                Math.abs(particle.x - targetX) > 0.12 ||
                Math.abs(particle.y - targetY) > 0.12 ||
                Math.abs(particle.vx) > 0.08 ||
                Math.abs(particle.vy) > 0.08
            ) {
                settled = false;
            }
        });

        draw();
        if (active || !settled) {
            window.requestAnimationFrame(animate);
        } else {
            running = false;
        }
    };

    const start = () => {
        if (running) return;
        running = true;
        window.requestAnimationFrame(animate);
    };

    const revealPixels = () => {
        if (revealed || reducedMotion.matches) return;
        revealed = true;
        word.classList.add("is-revealing");
        window.requestAnimationFrame(() => {
            window.requestAnimationFrame(() => word.classList.add("is-pixelated"));
        });
        window.setTimeout(() => word.classList.remove("is-revealing"), 2450);
    };

    const prepare = () => {
        buildParticles();
        revealTimer = window.setTimeout(revealPixels, 900);

        if (finePointer.matches) {
            word.addEventListener("pointerenter", (event) => {
                window.clearTimeout(revealTimer);
                revealPixels();
                const bounds = canvas.getBoundingClientRect();
                pointer = { x: event.clientX - bounds.left, y: event.clientY - bounds.top };
                active = true;
                start();
            });
            word.addEventListener("pointermove", (event) => {
                const bounds = canvas.getBoundingClientRect();
                pointer = { x: event.clientX - bounds.left, y: event.clientY - bounds.top };
            });
            word.addEventListener("pointerleave", () => {
                active = false;
                start();
            });
        }

        if ("ResizeObserver" in window) {
            new ResizeObserver(buildParticles).observe(word);
        } else {
            window.addEventListener("resize", buildParticles);
        }
    };

    reducedMotion.addEventListener("change", (event) => {
        if (!event.matches) return;
        window.clearTimeout(revealTimer);
        active = false;
        word.classList.remove("is-revealing", "is-pixelated");
    });

    if (document.fonts?.ready) {
        document.fonts.ready.then(prepare);
    } else {
        prepare();
    }
})();
