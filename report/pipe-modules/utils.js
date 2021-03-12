function processAssertions(data) {
  if (data.data.length > 0 && data.data[0].assertions) {
    const testCases = data.data;

    testCases.forEach(testCase => {
      const newAssertions = {};

      testCase.assertions.forEach(assertion => {
        newAssertions[assertion.processor] = assertion.result.outcome;
      });

      testCase.assertions = newAssertions;
    });
  }

  return data;
}

module.exports = {
  processAssertions
}
