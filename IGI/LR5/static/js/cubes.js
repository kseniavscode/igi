document.addEventListener('DOMContentLoaded', function () {

    class Cube {
        constructor(edge) {
            this._edge = parseFloat(edge);
        }

        // Method 1: Getter for edge
        get edge() {
            return this._edge;
        }

        // Method 2: Setter for edge
        set edge(value) {
            this._edge = parseFloat(value);
        }

        // Method 3: Volume calculation V = a^3
        getVolume() {
            return Math.pow(this._edge, 3);
        }
    }

    // 2. DERIVED CLASS: COLORED CUBE (Adds color parameter)
    class ColoredCubeClass extends Cube {
        constructor(edge, color) {
            super(edge); // Calls parent constructor
            this._color = color; // Additional parameter
        }

        // Method 4: Getter for color
        get color() {
            return this._color;
        }

        // Method 5: Setter for color
        set color(value) {
            this._color = value;
        }
    }


    // =========================================================================
    // VARIANT 2: FUNCTIONAL PROTOTYPE STYLE (Prototype Inheritance)
    // =========================================================================

    // 1. Base constructor function
    function ProtoCube(edge) {
        this._edge = parseFloat(edge);
    }
    ProtoCube.prototype.getEdge = function() { return this._edge; };
    ProtoCube.prototype.setEdge = function(val) { this._edge = parseFloat(val); };
    ProtoCube.prototype.getVolume = function() { return Math.pow(this._edge, 3); };

    // 2. Derived constructor function
    function ProtoColoredCube(edge, color) {
        ProtoCube.call(this, edge); // Inherits properties
        this._color = color;
    }
    // Prototype chain inheritance:
    ProtoColoredCube.prototype = Object.create(ProtoCube.prototype);
    ProtoColoredCube.prototype.constructor = ProtoColoredCube;

    ProtoColoredCube.prototype.getColor = function() { return this._color; };
    ProtoColoredCube.prototype.setColor = function(val) { this._color = val; };

    Object.defineProperty(ProtoColoredCube.prototype, 'edge', {
        get: function() { return this._edge; }
    });
    Object.defineProperty(ProtoColoredCube.prototype, 'color', {
        get: function() { return this._color; }
    });


    // =========================================================================
    // APPLICATION MANAGER (Collection Controller)
    // =========================================================================
    class CubeManager {
        constructor() {
            this.cubes = []; 
            this.currentMode = 'class'; // 'class' or 'prototype'

            this.tableBody = document.getElementById('cubes_table_body');
            this.countSpan = document.getElementById('cubes_count');
            this.resultBox = document.getElementById('result_output');
            this.form = document.getElementById('cube_form');
            this.edgeInput = document.getElementById('cube_edge');
            this.colorSelect = document.getElementById('cube_color');
            this.badge = document.getElementById('current_engine_badge');

            this.init();
        }

        init() {
            // Engine switcher (ES6 vs Prototype)
            document.querySelectorAll('input[name="oop_style"]').forEach(radio => {
                radio.addEventListener('change', (e) => {
                    this.currentMode = e.target.value;
                    this.badge.textContent = this.currentMode === 'class' ? 'Engine: ES6 Classes' : 'Engine: Prototypes';
                    this.badge.style.background = this.currentMode === 'class' ? '#aa8822' : '#2e7d32';
                });
            });

            // Form submit event
            this.form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.addCubeFromForm();
            });

            // Calculate button event
            document.getElementById('calc_btn').addEventListener('click', () => {
                this.calculateAndDisplayResult();
            });

            // Demo data button event
            document.getElementById('fill_demo_btn').addEventListener('click', () => {
                this.fillDemoData();
            });
        }

        addCubeFromForm() {
            const edge = this.edgeInput.value;
            const color = this.colorSelect.value;

            let cubeObj;
            if (this.currentMode === 'class') {
                cubeObj = new ColoredCubeClass(edge, color);
            } else {
                cubeObj = new ProtoColoredCube(edge, color);
            }

            this.cubes.push(cubeObj);
            this.renderTable();
            this.form.reset();
        }

        renderTable() {
            this.tableBody.innerHTML = '';
            this.countSpan.textContent = this.cubes.length;

            if (this.cubes.length === 0) {
                this.tableBody.innerHTML = `<tr><td colspan="4" style="text-align:center;">No cubes yet.</td></tr>`;
                return;
            }

            this.cubes.forEach((cube, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td><strong>${cube.edge}</strong> cm</td>
                    <td><span class="color_stat_badge badge_${cube.color}">${cube.color.toUpperCase()}</span></td>
                    <td>${cube.getVolume().toFixed(2)} cm³</td>
                `;
                this.tableBody.appendChild(row);
            });
        }

        calculateAndDisplayResult() {
            if (this.cubes.length === 0) {
                this.resultBox.innerHTML = '<span style="color:red;">⚠️ The collection is empty! Add at least one cube.</span>';
                return;
            }

            // Color counters
            const colorCounts = {
                red: 0,
                yellow: 0,
                blue: 0,
                green: 0
            };

            let totalVolume = 0;

            // Algorithm computation
            this.cubes.forEach(cube => {
                const color = cube.color;
                if (colorCounts.hasOwnProperty(color)) {
                    colorCounts[color]++;
                }
                totalVolume += cube.getVolume();
            });

            // Output rendering
            this.resultBox.innerHTML = `
                <h4>📊 Analysis Results (Variant 11):</h4>
                <p><strong>Cubes quantity by color:</strong></p>
                <ul>
                    <li><span class="color_stat_badge badge_red">RED:</span> <strong>${colorCounts.red}</strong> pcs</li>
                    <li><span class="color_stat_badge badge_yellow">YELLOW:</span> <strong>${colorCounts.yellow}</strong> pcs</li>
                    <li><span class="color_stat_badge badge_blue">BLUE:</span> <strong>${colorCounts.blue}</strong> pcs</li>
                    <li><span class="color_stat_badge badge_green">GREEN:</span> <strong>${colorCounts.green}</strong> pcs</li>
                </ul>
                <hr style="border:0; border-top:1px dashed #ccc; margin:10px 0;">
                <p style="font-size: 1.1em;">
                    📦 <strong>Total volume of all cubes:</strong> 
                    <span style="color:#7b5f0c; font-weight:bold;">${totalVolume.toFixed(2)} cm³</span>
                </p>
            `;
        }

        fillDemoData() {
            const demoCubes = [
                { edge: 3, color: 'red' },
                { edge: 5, color: 'green' },
                { edge: 2.5, color: 'blue' },
                { edge: 4, color: 'red' },
                { edge: 6, color: 'yellow' },
                { edge: 3, color: 'green' }
            ];

            demoCubes.forEach(d => {
                let c = this.currentMode === 'class' ? new ColoredCubeClass(d.edge, d.color) : new ProtoColoredCube(d.edge, d.color);
                this.cubes.push(c);
            });

            this.renderTable();
            this.calculateAndDisplayResult();
        }
    }

    new CubeManager();
});