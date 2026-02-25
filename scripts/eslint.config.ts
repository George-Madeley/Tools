import pluginJs from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import pluginImport from "eslint-plugin-import";
import pluginReact from "eslint-plugin-react";
import pluginReactHooks from "eslint-plugin-react-hooks";
import pluginImportSort from "eslint-plugin-simple-import-sort";
import globals from "globals";
import tseslint from "typescript-eslint";

/**
 * This is the esLinter configuration file that dictates how all of the
 * type/javascript files are formatted and linted.
 */
export default defineConfig([
  globalIgnores([
    "**/node_modules/*",
    "**/public/*",
    "**/build/*",
    "**/.react-router/*",
    "**/.next/*",
    "**/imports/*",
    "**/gen/*",
    "**/dist/*",
    "**/next-env.d.ts",
  ]),
  {
    files: ["**/*.{js,mjs,cjs,jsx,ts,mts,cts,tsx}"],
    plugins: { js: pluginJs },
    extends: ["js/recommended"],
    languageOptions: { globals: { ...globals.browser, ...globals.node } },
  },
  {
    languageOptions: {
      parserOptions: {
        tsconfigRootDir: __dirname,
      },
    },
  },
  tseslint.configs.recommended,
  tseslint.configs.stylistic,
  pluginReact.configs.flat.recommended,
  pluginReact.configs.flat["jsx-runtime"],
  pluginReactHooks.configs.flat["recommended-latest"],

  {
    files: ["{packages,scripts,web}/**/*.{js,cjs,mjs,jsx,ts,cts,mts,tsx}"],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      "simple-import-sort": pluginImportSort,
      import: pluginImport,
    },
    rules: {
      ...pluginReactHooks.configs.recommended.rules,
      "@typescript-eslint/no-empty-function": "off",
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unused-expressions": [
        "error",
        { allowShortCircuit: true, allowTernary: true },
      ],
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            { regex: "^@mui/[^/]+$" },
            { regex: "^@toolpad/[^/]+$" },
            { regex: "^@atl-ui/[^/]+$" },
          ],
        },
      ],
      "react/boolean-prop-naming": "error",
      "react/button-has-type": "error",
      "react/display-name": "error",
      "react/hook-use-state": "warn",
      "react/jsx-boolean-value": "warn",
      "react/jsx-handler-names": "warn",
      "react/jsx-pascal-case": "error",
      "react/jsx-sort-props": "warn",
      "react/jsx-uses-react": "error",
      "react/no-children-prop": "error",
      "react/no-danger-with-children": "error",
      "react/prefer-stateless-function": "error",
      "react/prop-types": "error",
      "simple-import-sort/imports": "warn",
      "simple-import-sort/exports": "warn",
      "import/first": "error",
      "import/newline-after-import": "error",
      "import/no-duplicates": "error",
    },
  },
]);
