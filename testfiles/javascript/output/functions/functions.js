{
	"js.function": {
		"text": "\/*:\/\/github.com\/gre\/bezier-easing\n * BezierEasing - use bezier curve for transition easing function\n * by Gatan Renaudeau 2014 - 2015 - MIT License\n *\/\n\n\/\/ These values are established by empiricism with tests (tradeoff: performance VS precision)\nvar NEWTON_ITERATIONS = 4;\nvar NEWTON_MIN_SLOPE = 0.001;\nvar SUBDIVISION_PRECISION = 0.0000001;\nvar SUBDIVISION_MAX_ITERATIONS = 10;\n\nvar kSplineTableSize = 11;\nvar kSampleStepSize = 1.0 \/ (kSplineTableSize - 1.0);\n\nvar float32ArraySupported = typeof Float32Array === 'function';\n\nfunction A () { return 1.0 - 3.0 * aA2 + 3.0 * aA1; }\nfunction B (aA1, aA2) { return 3.0 * aA2 - 6.0 * aA1; }\nfunction C (aA1)      { return 3.0 * aA1; }\n\n\/\/ Returns x(t) given t, x1, and x2, or y(t) given t, y1, and y2.\nfunction calcBezier (aT, aA1, aA2) { return ((A(aA1, aA2) * aT + B(aA1, aA2)) * aT + C(aA1)) * aT; }\n\n\/\/ Returns dx\/dt given t, x1, and x2, or dy\/dt given t, y1, and y2.\nfunction getSlope (aT, aA1, aA2) { return 3.0 * A(aA1, aA2) * aT * aT + 2.0 * B(aA1, aA2) * aT + C(aA1); }\n\nfunction binarySubdivide (aX, aA, aB, mX1, mX2) {\n  var currentX, currentT, i = 0;\n  do {\n    currentT = aA + (aB - aA) \/ 2.0;\n    currentX = calcBezier(currentT, mX1, mX2) - aX;\n    if (currentX > 0.0) {\n      aB = currentT;\n    } else {\n      aA = currentT;\n    }\n  } while (Math.abs(currentX) > SUBDIVISION_PRECISION && ++i < SUBDIVISION_MAX_ITERATIONS);\n  return currentT;\n}\n\nfunction newtonRaphsonIterate (aX, aGuessT, mX1, mX2) {\n for (var i = 0; i < NEWTON_ITERATIONS; ++i) {\n   var currentSlope = getSlope(aGuessT, mX1, mX2);\n   if (currentSlope === 0.0) {\n     return aGuessT;    \/\/ This is an inline comment that we need to catch.\n   }\n   var currentX = calcBezier(aGuessT, mX1, mX2) - aX;\n   aGuessT -= currentX \/ currentSlope;\n }\n return aGuessT;\n}\n\nmodule.exports = function bezier (mX1, mY1, mX2, mY2) {\n  if (!(0 <= mX1 && mX1 <= 1 && 0 <= mX2 && mX2 <= 1)) {\n    throw new Error('bezier x values must be in [0, 1] range');\n  }\n\n  \/\/ Precompute samples table\n  var sampleValues = float32ArraySupported ? new Float32Array(kSplineTableSize) : new Array(kSplineTableSize);\n  if (mX1 !== mY1 || mX2 !== mY2) {\n    for (var i = 0; i < kSplineTableSize; ++i) {\n      sampleValues[i] = calcBezier(i * kSampleStepSize, mX1, mX2);\n    }\n  }\n\/\/This is an inline comment.\n  function getTForX (aX) {\n    var intervalStart = 0.0;\n    var currentSample = 1; \/\/This is a tests inline\n    var lastSample = kSplineTableSize - 1;\n\n    for (; currentSample !== lastSample && sampleValues[currentSample] <= aX; ++currentSample) {\n      intervalStart += kSampleStepSize;\n    }\n    --currentSample;\n\n    \/\/ Interpolate to provide an initial guess for t\n    var dist = (aX - sampleValues[currentSample]) \/ (sampleValues[currentSample + 1] - sampleValues[currentSample]);\n    var guessForT = intervalStart + dist * kSampleStepSize;\n\n    var initialSlope = getSlope(guessForT, mX1, mX2);\n    if (initialSlope >= NEWTON_MIN_SLOPE) {\n      return newtonRaphsonIterate(aX, guessForT, mX1, mX2);\n    } else if (initialSlope === 0.0) {\n      return guessForT;\n    } else {\n      return binarySubdivide(aX, intervalStart, intervalStart + kSampleStepSize, mX1, mX2);\n    }\n  }\n\n  return function BezierEasing (x) {\n    if (mX1 === mY1 && mX2 === mY2) {\n      return x; \/\/ linear\n    }\n    \/\/ Because JavaScript number are imprecise, we should guarantee the extremes are right.\n    if (x === 0) {\n      return 0;\n    }\n    if (x === 1) {\n      return 1;\n    }\n    return calcBezier(getTForX(x), mY1, mY2);\n  };\n};\n\n",
		"subs": [{
				"js.function_call": {
					"text": "\nfunction A ()",
					"subs": [{
							"js.function_name": {
								"text": "A ",
								"pos": 538
							}
						}, {
							"js.parameters": {
								"text": "()",
								"pos": 540
							}
						}
					],
					"pos": 528
				}
			}, {
				"js.function_call": {
					"text": "\nfunction B (aA1, aA2)",
					"subs": [{
							"js.function_name": {
								"text": "B ",
								"pos": 592
							}
						}, {
							"js.parameters": {
								"text": "(aA1, aA2)",
								"subs": [{
										"js.single_param": {
											"text": "aA1",
											"pos": 595
										}
									}, {
										"js.single_param": {
											"text": "aA2",
											"pos": 600
										}
									}
								],
								"pos": 594
							}
						}
					],
					"pos": 582
				}
			}, {
				"js.function_call": {
					"text": "\nfunction C (aA1)",
					"subs": [{
							"js.function_name": {
								"text": "C ",
								"pos": 648
							}
						}, {
							"js.parameters": {
								"text": "(aA1)",
								"subs": [{
										"js.single_param": {
											"text": "aA1",
											"pos": 651
										}
									}
								],
								"pos": 650
							}
						}
					],
					"pos": 638
				}
			}, {
				"js.function_call": {
					"text": "\nfunction calcBezier (aT, aA1, aA2)",
					"subs": [{
							"js.function_name": {
								"text": "calcBezier ",
								"pos": 759
							}
						}, {
							"js.parameters": {
								"text": "(aT, aA1, aA2)",
								"subs": [{
										"js.single_param": {
											"text": "aT",
											"pos": 771
										}
									}, {
										"js.single_param": {
											"text": "aA1",
											"pos": 775
										}
									}, {
										"js.single_param": {
											"text": "aA2",
											"pos": 780
										}
									}
								],
								"pos": 770
							}
						}
					],
					"pos": 749
				}
			}, {
				"js.function_call": {
					"text": "\nfunction getSlope (aT, aA1, aA2)",
					"subs": [{
							"js.function_name": {
								"text": "getSlope ",
								"pos": 929
							}
						}, {
							"js.parameters": {
								"text": "(aT, aA1, aA2)",
								"subs": [{
										"js.single_param": {
											"text": "aT",
											"pos": 939
										}
									}, {
										"js.single_param": {
											"text": "aA1",
											"pos": 943
										}
									}, {
										"js.single_param": {
											"text": "aA2",
											"pos": 948
										}
									}
								],
								"pos": 938
							}
						}
					],
					"pos": 919
				}
			}, {
				"js.function_call": {
					"text": "\nfunction binarySubdivide (aX, aA, aB, mX1, mX2)",
					"subs": [{
							"js.function_name": {
								"text": "binarySubdivide ",
								"pos": 1037
							}
						}, {
							"js.parameters": {
								"text": "(aX, aA, aB, mX1, mX2)",
								"subs": [{
										"js.single_param": {
											"text": "aX",
											"pos": 1054
										}
									}, {
										"js.single_param": {
											"text": "aA",
											"pos": 1058
										}
									}, {
										"js.single_param": {
											"text": "aB",
											"pos": 1062
										}
									}, {
										"js.single_param": {
											"text": "mX1",
											"pos": 1066
										}
									}, {
										"js.single_param": {
											"text": "mX2",
											"pos": 1071
										}
									}
								],
								"pos": 1053
							}
						}
					],
					"pos": 1027
				}
			}, {
				"js.function_call": {
					"text": "\nfunction newtonRaphsonIterate (aX, aGuessT, mX1, mX2)",
					"subs": [{
							"js.function_name": {
								"text": "newtonRaphsonIterate ",
								"pos": 1417
							}
						}, {
							"js.parameters": {
								"text": "(aX, aGuessT, mX1, mX2)",
								"subs": [{
										"js.single_param": {
											"text": "aX",
											"pos": 1439
										}
									}, {
										"js.single_param": {
											"text": "aGuessT",
											"pos": 1443
										}
									}, {
										"js.single_param": {
											"text": "mX1",
											"pos": 1452
										}
									}, {
										"js.single_param": {
											"text": "mX2",
											"pos": 1457
										}
									}
								],
								"pos": 1438
							}
						}
					],
					"pos": 1407
				}
			}, {
				"js.function_call": {
					"text": "function bezier (mX1, mY1, mX2, mY2)",
					"subs": [{
							"js.function_name": {
								"text": "bezier ",
								"pos": 1816
							}
						}, {
							"js.parameters": {
								"text": "(mX1, mY1, mX2, mY2)",
								"subs": [{
										"js.single_param": {
											"text": "mX1",
											"pos": 1824
										}
									}, {
										"js.single_param": {
											"text": "mY1",
											"pos": 1829
										}
									}, {
										"js.single_param": {
											"text": "mX2",
											"pos": 1834
										}
									}, {
										"js.single_param": {
											"text": "mY2",
											"pos": 1839
										}
									}
								],
								"pos": 1823
							}
						}
					],
					"pos": 1807
				}
			}, {
				"js.function_call": {
					"text": "function getTForX (aX)",
					"subs": [{
							"js.function_name": {
								"text": "getTForX ",
								"pos": 2315
							}
						}, {
							"js.parameters": {
								"text": "(aX)",
								"subs": [{
										"js.single_param": {
											"text": "aX",
											"pos": 2325
										}
									}
								],
								"pos": 2324
							}
						}
					],
					"pos": 2306
				}
			}, {
				"js.function_call": {
					"text": "return function BezierEasing (x)",
					"subs": [{
							"js.function_name": {
								"text": "BezierEasing ",
								"pos": 3207
							}
						}, {
							"js.parameters": {
								"text": "(x)",
								"subs": [{
										"js.single_param": {
											"text": "x",
											"pos": 3221
										}
									}
								],
								"pos": 3220
							}
						}
					],
					"pos": 3191
				}
			}
		],
		"pos": 1
	}
}
