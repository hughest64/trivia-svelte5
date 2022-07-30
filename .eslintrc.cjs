module.exports = {
	root: true,
	parser: '@typescript-eslint/parser',
	extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended', 'prettier'],
	plugins: ['svelte3', '@typescript-eslint'],
	ignorePatterns: ['*.cjs'],
	overrides: [{ files: ['*.svelte'], processor: 'svelte3/svelte3' }],
	settings: {
		'svelte3/typescript': () => require('typescript'),
	},
	parserOptions: {
		sourceType: 'module',
		ecmaVersion: 2020
	},
	env: {
		browser: true,
		es2017: true,
		node: true
	},
	rules: {
		'array-bracket-spacing': ['warn', 'never'],
		'arrow-parens': 'warn',
		'eqeqeq': ['error', 'smart'],
		'indent': ['warn', 4, { 'SwitchCase': 1 }],
		'max-len': ['warn', { code: 120 }],
		'no-extra-boolean-cast': 'off',
		'no-var': 'error',
		'object-curly-spacing': ['warn', 'always'],
		'prefer-arrow-callback': 'warn',
		'quotes': ['warn', 'single'],
		'radix': 'error',
		'semi': ['warn', 'always'],
		'spaced-comment': ['warn', 'always', { 'markers': ['/'] }],
	}
};
