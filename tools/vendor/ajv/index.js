export class SimpleAjv {
  constructor(options = {}) {
    this.options = options;
    this.formats = new Map();
  }

  addFormat(name, validate) {
    this.formats.set(name, typeof validate === 'function' ? validate : () => true);
  }

  compile(schema) {
    const rootSchema = schema;
    const formats = this.formats;

    const validator = (data) => {
      const errors = [];
      validateNode(rootSchema, data, '', errors, rootSchema, formats);
      validator.errors = errors.length ? errors : null;
      return errors.length === 0;
    };

    return validator;
  }
}

function validateNode(schema, data, path, errors, rootSchema, formats) {
  if (!schema || typeof schema !== 'object') {
    return;
  }

  if (schema.$ref) {
    const target = resolveRef(schema.$ref, rootSchema);
    if (!target) {
      errors.push({ instancePath: path, message: `unable to resolve reference ${schema.$ref}` });
      return;
    }
    validateNode(target, data, path, errors, rootSchema, formats);
    return;
  }

  if (schema.type) {
    if (!matchesType(schema.type, data)) {
      errors.push({ instancePath: path || '/', message: `must be of type ${schema.type}` });
      return;
    }
  }

  if (schema.enum && !schema.enum.includes(data)) {
    errors.push({ instancePath: path || '/', message: `must be equal to one of the allowed values` });
  }

  if (schema.pattern && typeof data === 'string') {
    const re = new RegExp(schema.pattern);
    if (!re.test(data)) {
      errors.push({ instancePath: path || '/', message: `must match pattern ${schema.pattern}` });
    }
  }

  if (schema.minLength != null && typeof data === 'string') {
    if (data.length < schema.minLength) {
      errors.push({ instancePath: path || '/', message: `must NOT have fewer than ${schema.minLength} characters` });
    }
  }

  if (schema.minimum != null && typeof data === 'number') {
    if (data < schema.minimum) {
      errors.push({ instancePath: path || '/', message: `must be >= ${schema.minimum}` });
    }
  }

  if (schema.format && typeof data === 'string') {
    const formatValidator = formats.get(schema.format);
    if (formatValidator && !formatValidator(data)) {
      errors.push({ instancePath: path || '/', message: `must match format ${schema.format}` });
    }
  }

  if (schema.type === 'object') {
    const props = schema.properties ?? {};
    const required = schema.required ?? [];

    for (const key of required) {
      if (data == null || Object.prototype.hasOwnProperty.call(data, key) === false) {
        errors.push({ instancePath: path || '/', message: `must have required property '${key}'` });
      }
    }

    if (schema.additionalProperties === false && data && typeof data === 'object') {
      for (const key of Object.keys(data)) {
        if (!Object.prototype.hasOwnProperty.call(props, key)) {
          errors.push({ instancePath: joinPath(path, key), message: 'must NOT have additional properties' });
        }
      }
    }

    for (const [key, subschema] of Object.entries(props)) {
      if (data && Object.prototype.hasOwnProperty.call(data, key)) {
        validateNode(subschema, data[key], joinPath(path, key), errors, rootSchema, formats);
      }
    }
  }

  if (schema.type === 'array' && Array.isArray(data)) {
    if (schema.minItems != null && data.length < schema.minItems) {
      errors.push({ instancePath: path || '/', message: `must NOT have fewer than ${schema.minItems} items` });
    }
    if (schema.items) {
      data.forEach((item, index) => {
        validateNode(schema.items, item, joinPath(path, index), errors, rootSchema, formats);
      });
    }
  }
}

function matchesType(expected, value) {
  if (Array.isArray(expected)) {
    return expected.some((type) => matchesType(type, value));
  }
  switch (expected) {
    case 'object':
      return value !== null && typeof value === 'object' && !Array.isArray(value);
    case 'array':
      return Array.isArray(value);
    case 'string':
      return typeof value === 'string';
    case 'integer':
      return Number.isInteger(value);
    case 'number':
      return typeof value === 'number';
    case 'boolean':
      return typeof value === 'boolean';
    default:
      return true;
  }
}

function resolveRef(ref, rootSchema) {
  if (!ref.startsWith('#/')) {
    return null;
  }
  const pathParts = ref
    .slice(2)
    .split('/')
    .map((part) => part.replace(/~1/g, '/').replace(/~0/g, '~'));
  let current = rootSchema;
  for (const part of pathParts) {
    if (current && typeof current === 'object' && Object.prototype.hasOwnProperty.call(current, part)) {
      current = current[part];
    } else {
      return null;
    }
  }
  return current;
}

function joinPath(base, key) {
  if (base === '') {
    return `/${key}`;
  }
  return `${base}/${key}`;
}

export default SimpleAjv;
