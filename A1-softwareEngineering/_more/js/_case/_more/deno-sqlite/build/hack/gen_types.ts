interface Item {
  name: string;
  arguments: Argument[];
  returnType: Type;
}

interface Argument {
  name: string;
  type: Type;
}

enum Type {
  Void,
  VoidPtr,
  StringPtr,
  StatementPtr,
  Double,
  Int,
}

const items = [
  // exported manually in compiler invocation
  {
    name: "malloc",
    arguments: [{ name: "size", type: Type.Int }],
    returnType: Type.VoidPtr,
  },
  {
    name: "free",
    arguments: [{ name: "ptr", type: Type.VoidPtr }],
    returnType: Type.Void,
  },
];

const [src, dest] = Deno.args;
const wrapperSrc = await Deno.readTextFile(src);

// int EXPORT(bind_int) (sqlite3_stmt* stmt, int idx, double value)
const typeRegexp =
  `(const +)?(sqlite3_stmt\\*|char\\*|void\\*|int|uint32_t|double|void)`;
const argRegexp = `${typeRegexp} +[a-z_]+`;
const exportSignature = new RegExp(
  `${typeRegexp} +EXPORT\\([a-z_]+\\) +\\(((${argRegexp}( *, *${argRegexp})*)|)\\)`,
);

function nullThrows<T>(value: T | null | undefined): T {
  if (value == null) {
    throw new Error("Got a null value");
  }
  return value as T;
}

function typeFromCType(cType: string): Type {
  cType = cType.replace("const", "").replace(/ /g, "");
  switch (cType) {
    case "void":
      return Type.Void;
    case "void*":
      return Type.VoidPtr;
    case "char*":
      return Type.StringPtr;
    case "sqlite3_stmt*":
      return Type.StatementPtr;
    case "double":
      return Type.Double;
    case "int":
    case "uint32_t":
      return Type.Int;
    default:
      throw new Error("Unknown type");
  }
}

function getReturnType(line: string): Type {
  const regexp = new RegExp(typeRegexp);
  const [, _const, cType] = nullThrows(regexp.exec(line));
  return typeFromCType(cType);
}

function getName(line: string): string {
  const [, name] = nullThrows(/EXPORT\(([a-z_]+)\)/.exec(line));
  return name;
}

function getArguments(line: string): Argument[] {
  const [, argList] = nullThrows(/EXPORT\([a-z_]+\) *\(([^)]*)\)/.exec(line));
  if (argList.length === 0) {
    return [];
  } else {
    return argList.split(",").map((arg) => {
      const regexp = new RegExp(`${typeRegexp} +([a-z_]+)`);
      const [, _const, cType, name] = nullThrows(regexp.exec(arg));
      return {
        name,
        type: typeFromCType(cType),
      };
    });
  }
}

function generateType(tp: Type): string {
  switch (tp) {
    case Type.Void:
      return "void";
    case Type.VoidPtr:
      return "VoidPtr";
    case Type.StringPtr:
      return "StringPtr";
    case Type.StatementPtr:
      return "StatementPtr";
    case Type.Int:
    case Type.Double:
      return "number";
    default:
      throw new Error("Unknown type");
  }
}

function generateDecl(item: Item): string {
  const args = item.arguments.map((arg) =>
    `${arg.name}: ${generateType(arg.type)}`
  ).join(", ");
  return `${item.name}: (${args}) => ${generateType(item.returnType)}`;
}

const exportLines = wrapperSrc.split("\n").filter((line) =>
  exportSignature.test(line)
);

for (const line of exportLines) {
  const name = getName(line);
  const returnType = getReturnType(line);
  const args = getArguments(line);

  items.push({ name, returnType, arguments: args });
}

const typeDeclaration = `// Deno SQLite WASM binding types

export type VoidPtr = number;
export type StringPtr = number;
export type StatementPtr = number;

export interface Wasm {
  memory: WebAssembly.Memory;

  ${items.map(generateDecl).join(";\n  ")};
}

export default function instantiate(): { exports: Wasm };
`;

await Deno.writeTextFile(dest, typeDeclaration);
