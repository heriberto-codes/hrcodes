(() => {
  const builderForm = document.querySelector("[data-builder-form]");
  if (!builderForm) return;

  const steps = [...builderForm.querySelectorAll("[data-step]")];
  const progressButtons = [...document.querySelectorAll("[data-step-target]")];
  const summary = {
    area: document.querySelector('[data-summary="area"]'),
    stage: document.querySelector('[data-summary="stage"]'),
    goal: document.querySelector('[data-summary="goal"]'),
  };
  let currentStep = 1;
  let furthestStep = 1;

  const currentPanel = () => steps.find((step) => Number(step.dataset.step) === currentStep);

  const validatePanel = (panel) => {
    builderForm.classList.add("was-validated");
    const invalid = [...panel.querySelectorAll("[required]")].find((field) => !field.checkValidity());
    if (invalid) {
      invalid.focus();
      return false;
    }
    return true;
  };

  const showStep = (stepNumber) => {
    currentStep = stepNumber;
    furthestStep = Math.max(furthestStep, currentStep);
    builderForm.classList.remove("was-validated");

    steps.forEach((step) => {
      const active = Number(step.dataset.step) === currentStep;
      step.hidden = !active;
      step.classList.toggle("is-active", active);
    });

    progressButtons.forEach((button) => {
      const target = Number(button.dataset.stepTarget);
      const active = target === currentStep;
      button.disabled = target > furthestStep;
      button.classList.toggle("is-active", active);
      if (active) button.setAttribute("aria-current", "step");
      else button.removeAttribute("aria-current");
    });

    currentPanel()?.querySelector("h2")?.focus({ preventScroll: true });
    currentPanel()?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  };

  builderForm.addEventListener("change", (event) => {
    const field = event.target;
    if (field.name === "builder-area" && summary.area) summary.area.textContent = field.value;
    if (field.name === "builder-stage" && summary.stage) summary.stage.textContent = field.value;
  });

  builderForm.addEventListener("input", (event) => {
    if (event.target.name !== "builder-goal" || !summary.goal) return;
    const text = event.target.value.trim();
    summary.goal.textContent = text ? `${text.slice(0, 72)}${text.length > 72 ? "…" : ""}` : "Add in step two";
  });

  builderForm.addEventListener("click", (event) => {
    const next = event.target.closest("[data-next-step]");
    const back = event.target.closest("[data-back-step]");
    if (next && validatePanel(currentPanel())) showStep(Math.min(3, currentStep + 1));
    if (back) showStep(Math.max(1, currentStep - 1));
  });

  progressButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const target = Number(button.dataset.stepTarget);
      if (target <= furthestStep) showStep(target);
    });
  });

  builderForm.addEventListener("submit", (event) => {
    event.preventDefault();
    builderForm.classList.add("was-validated");
    if (!builderForm.checkValidity()) {
      const invalid = builderForm.querySelector(":invalid");
      invalid?.focus();
      return;
    }

    const status = document.querySelector("[data-builder-status]");
    builderForm.hidden = true;
    document.querySelector(".step-progress")?.setAttribute("hidden", "");
    status?.setAttribute("aria-hidden", "false");
    status?.focus();
  });

  document.querySelector("[data-reset-builder]")?.addEventListener("click", () => {
    builderForm.reset();
    builderForm.hidden = false;
    builderForm.classList.remove("was-validated");
    document.querySelector(".step-progress")?.removeAttribute("hidden");
    document.querySelector("[data-builder-status]")?.setAttribute("aria-hidden", "true");
    if (summary.area) summary.area.textContent = "Not selected yet";
    if (summary.stage) summary.stage.textContent = "Not selected yet";
    if (summary.goal) summary.goal.textContent = "Add in step two";
    currentStep = 1;
    furthestStep = 1;
    showStep(1);
  });
})();
