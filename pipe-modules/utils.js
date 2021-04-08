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

function formatDate(data) {
  if (data.data.length > 0 && data.data[0].version) {
    data.data.forEach(processor => {
      const date = new Date(processor.date);
      const day = ('' + date.getDate()).padStart(2, '0');
      const month = ('' + (date.getMonth() + 1)).padStart(2, '0');

      processor.date = date.getFullYear() + '-' + month + '-' + day;
    });
  }

  return data;
}

module.exports = {
  processAssertions,
  formatDate
}
