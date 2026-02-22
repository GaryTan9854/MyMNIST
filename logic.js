// Write a function that converts Celsius to Fahrenheit
// Formula: (celsius * 9/5) + 32

/**
 * Converts Celsius to Fahrenheit.
 * @param {number} celsius
 * @returns {number}
 */
function convertToFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

// Test the function with 30 degrees
console.log(`30 Celsius is ${convertToFahrenheit(30)} Fahrenheit`);
