const numberSteppers = document.querySelectorAll(".number-stepper");

function countDecimalPrecision(value) {
    const text = String(value);
    if (!text.includes(".")) {
        return 0;
    }
    return text.split(".")[1].length;
}

function clampValue(value, min, max) {
    let result = value;
    if (min !== null) {
        result = Math.max(result, min);
    }
    if (max !== null) {
        result = Math.min(result, max);
    }
    return result;
}

numberSteppers.forEach(function (stepper) {
    const input = stepper.querySelector('input[type="number"]');
    const decrementButton = stepper.querySelector('[data-stepper-action="decrement"]');
    const incrementButton = stepper.querySelector('[data-stepper-action="increment"]');
    let repeatInterval = null;

    if (!input || !decrementButton || !incrementButton) {
        return;
    }

    function startRepeating(direction) {
        if (repeatInterval !== null) {
            clearInterval(repeatInterval);
        }
        updateInput(direction);
        repeatInterval = setInterval(function () {
            updateInput(direction);
        }, 100);
    }

    function stopRepeating() {
        clearInterval(repeatInterval);
        repeatInterval = null;
    }

    function updateInput(direction) {
        const step = (input.step && input.step !== "any") ? Number(input.step) : 1;
        const min = input.min !== "" ? Number(input.min) : null;
        const max = input.max !== "" ? Number(input.max) : null;
        const currentValue = input.value === "" ? 0 : Number(input.value);

        if (Number.isNaN(currentValue)) {
            return;
        }

        const nextValue = clampValue(currentValue + direction * step, min, max);
        const decimals = countDecimalPrecision(step);
        input.value = String(Number(nextValue.toFixed(decimals)));

        input.dispatchEvent(new Event("input", {bubbles: true}));
        input.dispatchEvent(new Event("change", {bubbles: true}));
    }

    decrementButton.addEventListener("pointerdown", function () {
        startRepeating(-1);
    });

    decrementButton.addEventListener("pointerup", function () {
        stopRepeating();
    });

    decrementButton.addEventListener("pointerleave", function () {
        stopRepeating();
    });

    incrementButton.addEventListener("pointerdown", function () {
        startRepeating(1);
    });

    incrementButton.addEventListener("pointerup", function () {
        stopRepeating();
    });

    incrementButton.addEventListener("pointerleave", function () {
        stopRepeating();
    });
});