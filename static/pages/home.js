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
    const section = document.querySelector("[data-home-case-studies]");
    if (!section) return;

    const tabs = [...section.querySelectorAll("[role='tab']")];
    const panels = [...section.querySelectorAll("[data-home-case-panel]")];
    const indexes = [...section.querySelectorAll("[data-home-case-index]")];
    if (!tabs.length || tabs.length !== panels.length) return;

    const selectTab = (tab, { moveFocus = false, preserveViewport = false } = {}) => {
        const tabTop = preserveViewport ? tab.getBoundingClientRect().top : 0;

        tabs.forEach((item) => {
            const selected = item === tab;
            item.setAttribute("aria-selected", String(selected));
            item.tabIndex = selected ? 0 : -1;
        });

        panels.forEach((panel) => {
            panel.hidden = panel.id !== tab.getAttribute("aria-controls");
        });

        indexes.forEach((index) => {
            index.hidden = index.dataset.homeCaseIndex !== tab.id;
        });

        if (moveFocus) tab.focus({ preventScroll: preserveViewport });

        if (preserveViewport) {
            window.requestAnimationFrame(() => {
                const scrollCorrection = tab.getBoundingClientRect().top - tabTop;
                if (Math.abs(scrollCorrection) > 1) {
                    window.scrollBy({ top: scrollCorrection, left: 0, behavior: "instant" });
                }
            });
        }
    };

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => selectTab(tab, { preserveViewport: true }));
        tab.addEventListener("keydown", (event) => {
            if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;

            event.preventDefault();
            let nextIndex = index;
            if (event.key === "ArrowLeft") nextIndex = (index - 1 + tabs.length) % tabs.length;
            if (event.key === "ArrowRight") nextIndex = (index + 1) % tabs.length;
            if (event.key === "Home") nextIndex = 0;
            if (event.key === "End") nextIndex = tabs.length - 1;
            selectTab(tabs[nextIndex], { moveFocus: true, preserveViewport: true });
        });
    });

    const selectTabForHash = () => {
        const selectedTab = window.location.hash === "#case-cthink" ? tabs[1] : tabs[0];
        selectTab(selectedTab);
    };

    section.classList.add("is-enhanced");
    selectTabForHash();
    window.addEventListener("hashchange", selectTabForHash);
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

(() => {
    const section = document.querySelector("[data-home-project]");
    if (!section) return;

    const builder = section.querySelector("[data-home-brief-builder]");
    const form = section.querySelector("[data-home-project-form]");
    if (!builder || !form) return;

    const steps = [...form.querySelectorAll("[data-home-step]")];
    const progress = section.querySelector("[data-home-project-progress]");
    const progressButtons = [...section.querySelectorAll("[data-home-step-target]")];
    const success = section.querySelector("[data-home-project-success]");
    const summary = {
        area: section.querySelector('[data-home-summary="area"]'),
        stage: section.querySelector('[data-home-summary="stage"]'),
        goal: section.querySelector('[data-home-summary="goal"]'),
    };
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const parsedInitialStep = Number(form.dataset.initialStep);
    let currentStep = Number.isInteger(parsedInitialStep) && parsedInitialStep >= 1 && parsedInitialStep <= steps.length
        ? parsedInitialStep
        : 1;
    let furthestStep = currentStep;

    const panelFor = (stepNumber) => steps.find((step) => Number(step.dataset.homeStep) === stepNumber);

    const controlsFor = (panel) => [...panel.querySelectorAll("input, select, textarea")]
        .filter((control) => control.type !== "hidden" && !control.disabled)
        .filter((control) => control.type !== "radio" || control.required);

    const controlsInGroup = (control, group) => {
        if (control.type !== "radio" || !control.name) return [control];
        return [...group.querySelectorAll(`input[type="radio"][name="${control.name}"]`)];
    };

    const updateFieldState = (control, invalid) => {
        const group = control.closest("[data-home-field-group]");
        if (!group) return;

        group.classList.toggle("has-error", invalid);
        controlsInGroup(control, group).forEach((field) => {
            if (invalid) field.setAttribute("aria-invalid", "true");
            else field.removeAttribute("aria-invalid");
        });

        const error = group.querySelector("[data-home-field-error]");
        if (error) {
            error.hidden = !invalid;
            error.classList.toggle("is-visible", invalid);
        }
    };

    const validatePanel = (panel, { focus = true } = {}) => {
        if (!panel) return true;

        let firstInvalid = null;
        controlsFor(panel).forEach((control) => {
            const invalid = !control.checkValidity();
            updateFieldState(control, invalid);
            if (invalid && !firstInvalid) firstInvalid = control;
        });

        if (firstInvalid && focus) firstInvalid.focus();
        return !firstInvalid;
    };

    const showStep = (stepNumber, { focusHeading = false, scroll = false } = {}) => {
        currentStep = stepNumber;
        furthestStep = Math.max(furthestStep, currentStep);

        steps.forEach((step) => {
            const active = Number(step.dataset.homeStep) === currentStep;
            step.hidden = !active;
            step.classList.toggle("is-active", active);
        });

        progressButtons.forEach((button) => {
            const target = Number(button.dataset.homeStepTarget);
            const active = target === currentStep;
            button.disabled = target > furthestStep;
            button.classList.toggle("is-active", active);
            if (active) button.setAttribute("aria-current", "step");
            else button.removeAttribute("aria-current");
        });

        const activePanel = panelFor(currentStep);
        if (focusHeading) activePanel?.querySelector("h3")?.focus({ preventScroll: true });
        if (scroll) activePanel?.scrollIntoView({ behavior: reducedMotion.matches ? "auto" : "smooth", block: "nearest" });
    };

    const updateChoiceSummary = (name, target) => {
        const selected = form.querySelector(`input[name="${name}"]:checked`);
        if (target) target.textContent = selected?.dataset.summaryValue || "Not selected yet";
    };

    const updateGoalSummary = () => {
        const goal = form.elements.goal;
        if (!goal || !summary.goal) return;
        const value = goal.value.trim();
        summary.goal.textContent = value ? `${value.slice(0, 72)}${value.length > 72 ? "…" : ""}` : "Add in step two";
    };

    const updateSummary = () => {
        updateChoiceSummary("work_area", summary.area);
        updateChoiceSummary("project_stage", summary.stage);
        updateGoalSummary();
    };

    builder.classList.add("is-enhanced");
    form.noValidate = true;
    showStep(currentStep);
    updateSummary();

    form.addEventListener("click", (event) => {
        const next = event.target.closest("[data-home-next-step]");
        const back = event.target.closest("[data-home-back-step]");

        if (next && validatePanel(panelFor(currentStep))) {
            showStep(Math.min(steps.length, currentStep + 1), { focusHeading: true, scroll: true });
        }
        if (back) showStep(Math.max(1, currentStep - 1), { focusHeading: true, scroll: true });
    });

    progressButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const target = Number(button.dataset.homeStepTarget);
            if (target <= furthestStep) showStep(target, { focusHeading: true, scroll: true });
        });
    });

    form.addEventListener("change", (event) => {
        const control = event.target;
        if (!(control instanceof HTMLInputElement || control instanceof HTMLSelectElement || control instanceof HTMLTextAreaElement)) return;

        if (control.name === "work_area") updateChoiceSummary("work_area", summary.area);
        if (control.name === "project_stage") updateChoiceSummary("project_stage", summary.stage);
        if (control.checkValidity()) updateFieldState(control, false);
    });

    form.addEventListener("input", (event) => {
        const control = event.target;
        if (!(control instanceof HTMLInputElement || control instanceof HTMLTextAreaElement)) return;

        if (control.name === "goal") updateGoalSummary();
        if (control.checkValidity()) updateFieldState(control, false);
    });

    form.addEventListener("submit", (event) => {
        let firstInvalidStep = null;
        let firstInvalidControl = null;

        steps.forEach((step) => {
            const valid = validatePanel(step, { focus: false });
            if (!valid && firstInvalidStep === null) {
                firstInvalidStep = Number(step.dataset.homeStep);
                firstInvalidControl = controlsFor(step).find((control) => !control.checkValidity());
            }
        });

        if (firstInvalidStep !== null) {
            event.preventDefault();
            showStep(firstInvalidStep, { scroll: true });
            firstInvalidControl?.focus({ preventScroll: true });
        }
    });

    if (success) {
        builder.classList.add("is-complete");
        window.requestAnimationFrame(() => success.focus({ preventScroll: true }));
    } else if (form.dataset.hasErrors === "true") {
        window.requestAnimationFrame(() => {
            const wideError = form.querySelector("[data-home-form-wide-error]");
            const invalid = panelFor(currentStep)?.querySelector('[aria-invalid="true"]');
            (wideError || invalid)?.focus({ preventScroll: true });
        });
    }

    section.querySelector("[data-home-reset-project]")?.addEventListener("click", () => {
        form.reset();
        form.querySelectorAll("[data-home-field-group]").forEach((group) => group.classList.remove("has-error"));
        form.querySelectorAll('[aria-invalid="true"]').forEach((control) => control.removeAttribute("aria-invalid"));
        form.querySelectorAll("[data-home-field-error]").forEach((error) => {
            error.hidden = true;
            error.classList.remove("is-visible");
        });
        success.hidden = true;
        builder.classList.remove("is-complete");
        currentStep = 1;
        furthestStep = 1;
        updateSummary();
        showStep(1, { focusHeading: true });
        progress?.scrollIntoView({ behavior: reducedMotion.matches ? "auto" : "smooth", block: "nearest" });
    });
})();
