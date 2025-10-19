export default function addFormats(ajv) {
  if (ajv && typeof ajv.addFormat === 'function') {
    ajv.addFormat('date-time', (value) => {
      if (typeof value !== 'string') {
        return false;
      }
      const timestamp = Date.parse(value);
      return Number.isFinite(timestamp);
    });
  }
  return ajv;
}

export function addFormatsFn(ajv) {
  return addFormats(ajv);
}
