  // TODO: make this an injected variable
  const RCE_ADDR = "http://127.0.0.1:8080";
  const LANGUAGE_TEMPLATES = {
    python: `
import numpy as np

def householder(a):
  """
  Computes the Householder transformation of a vector \`a\`.
  Given an m-dimensional vector a, the mxm Householder
  transformation matrix Q is defined as
      Q = I - 2 * v * vT
  where
      v = u / ||u||
      u = x - norm(x) * e_1
  """
  u = a.copy()
  u[0] += np.copysign(np.linalg.norm(a), a[0])
  u_0 = u[0]
  if u_0 == 0:
      u_0 = 1
  v = np.reshape(u / u_0, (-1, 1))

  I = np.eye(a.shape[0])
  vTv = np.dot(v.T, v)
  if vTv == 0:
      vTv = 1
  Q = I - (2 / vTv) * np.dot(v, v.T)
  return Q

def qr_decomposition(A):
  """
  Computes the QR decomposition of a matrix A.
  """
  m, n = A.shape
  R = A.copy()
  Q = np.eye(m)
  for i in range(min(m, n)):
      H = np.eye(m)
      H[i:, i:] = householder(R[i:, i])
      Q = np.dot(Q, H)
      R = np.dot(H, R)
  return Q, R

A = np.array([
 [1, 2, 3],
 [4, 5, 6],
 [7, 8, 9],
 [10, 11, 12],
 [13, 14, 15],
])
Q, R = qr_decomposition(A)

print("Q =", Q)
print("R =", R)
print("A = QR =", np.dot(Q, R))
`.trim(),
    javascript: `
// Derived from Rado Kirov's blog on incremental computation:
// https://rkirov.github.io/posts/incremental_computation
const {of, Subject} = require('rxjs');
const {map, switchMap, distinctUntilChanged} = require('rxjs/operators');

function doSquare(n) { return n * n; }
function doSqrt(n) { return Math.sqrt(n); }

const sq = new Subject();
const sqrt = new Subject();
const whichOp = new Subject();

const opSq = sq.pipe(map(doSquare), distinctUntilChanged());
const opSqrt = sqrt.pipe(map(doSqrt), distinctUntilChanged());
const op = whichOp.pipe(
    switchMap(which => which === 'sq' ? opSq : opSqrt));

op.subscribe((value) => console.log(\`recomputed: $\{value\}\`));

// initial computation for "sq"
op.next('sq');
sq.next(4);
sqrt.next(4);

// re-computation of "opSqrt" with new value
sqrt.next(16);  // no log occurs

// re-computation of "opSq" with new value
sq.next(16);  // log occurs
`.trim(),
    rust: `
use rand::Rng;
use rand::distributions::{Distribution, Standard};

/// A point in the unit square.
struct PointI2 {
    x: f64,
    y: f64,
}
impl Distribution<PointI2> for Standard {
    fn sample<R: Rng + ?Sized>(&self, rng: &mut R) -> PointI2 {
        PointI2 {
            x: rng.gen_range(0., 1.),
            y: rng.gen_range(0., 1.),
        }
    }
}

fn monte_carlo_pi(sample_size: u64) -> f64 {
    let in_unit_circle = |point: &PointI2| {
        let dx = point.x - 0.5;
        let dy = point.y - 0.5;
        (dx * dx) + (dy * dy) <= 0.25
    };
    let mut rng = rand::thread_rng();

    let num_in_circle = (0..sample_size)
        .map(|_| rng.gen::<PointI2>())
        .filter(in_unit_circle)
        .count() as f64;
    num_in_circle / (sample_size as f64) * 4.
}

fn main() {
    for mag in 3..6 {
        let sample_size = 10_u64.pow(mag);
        let estimate = monte_carlo_pi(sample_size);
        println!("[sample={}]\\t\\tpi ~= {}", sample_size, estimate);
    }
}`.trim(),
    cpp: `
#include <iostream>

int main() {
  std::cout << "Hello, world!\\n";
}`.trim(),
  };
  const DEFAULT_LANGUAGE = "python";

  require.config({ paths: { vs: "https://unpkg.com/monaco-editor@0.21.2/min/vs" } });
  window.MonacoEnvironment = { getWorkerUrl: () => proxy };

  const proxy = URL.createObjectURL(
    new Blob(
      [
        `
  	self.MonacoEnvironment = { baseUrl: 'https://unpkg.com/monaco-editor@0.21.2/min/' };
  	importScripts('https://unpkg.com/monaco-editor@0.21.2/min/vs/base/worker/workerMain.js');`,
      ],
      { type: "text/javascript" }
    )
  );

  const $ = document.querySelector.bind(document);

  require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create($("#playground"), {
      value: LANGUAGE_TEMPLATES[DEFAULT_LANGUAGE],
      language: DEFAULT_LANGUAGE,
      theme: "vs-dark",
      fontSize: "15px",
      padding: { top: "20px" },
    });
  });

  const ansi = new AnsiUp();
  ansi.use_classes = true;

  const ExecutionResult = {
    loading: () => {
      return { loading: true };
    },
    success: (exitCode, stdout, stderr) => {
      return { success: true, exitCode, stdout, stderr };
    },
    failure: () => {
      return { failure: true };
    },
  };

  Vue.component("results", {
    props: ["result"],
    template: `
      {% raw %}
      <div v-if="result.loading">
        <h2><span>Loading</span><span class="AnimatedEllipsis"></span></h2>
      </div>
      <div v-else>
        <div v-if="result.success">
          <h2>exit code</h2>
          <pre>{{ result.exitCode }}</pre>
          <h2>stdout</h2>
          <component :is="stdoutHtml"></component>
          <h2>stderr</h2>
          <component :is="stderrHtml"></component>
        </div>
        <div v-else>
          <h2>Loading Error</h2>
          Please try again.
        </div>
      </div>
      {% endraw %}
    `,
    computed: {
      stdoutHtml() {
        const stdout = ansi.ansi_to_html(this.result.stdout);
        return {
          template: `<pre class="inner">${stdout}</pre>`,
        };
      },
      stderrHtml() {
        const stderr = ansi.ansi_to_html(this.result.stderr);
        return {
          template: `<pre class="inner">${stderr}</pre>`,
        };
      },
    },
  });

  const DescriptionResult = {
    loading: () => {
      return { loading: true };
    },
    success: (languageDescription, osVersion, packages) => {
      return { success: true, languageDescription, osVersion, packages };
    },
    failure: () => {
      return { failure: true };
    },
  };

  Vue.component("description", {
    props: ["result"],
    template: `
      {% raw %}
      <div v-if="result.loading">
        <span>Loading</span><span class="AnimatedEllipsis"></span>
      </div>
      <div v-else>
        <div v-if="result.success">
          <b>{{ result.languageDescription }} - {{ result.osVersion }}</b>
          <pre class="mb-0">{{ result.packages.join('\\n') }}</pre>
        </div>
        <div v-else>
          <h2>Loading Error</h2>
          Please try again.
        </div>
      </div>
      {% endraw %}
    `,
  });

  new Vue({
    el: "#app",
    data: {
      language: DEFAULT_LANGUAGE,
      lastLanguage: DEFAULT_LANGUAGE,
      languageOptions: Object.keys(LANGUAGE_TEMPLATES),
      executionResult: ExecutionResult.success("", "", ""),
      descriptionResult: DescriptionResult.success("", "", []),
    },
    methods: {
      async run() {
        this.executionResult = ExecutionResult.loading();
        await axios
          .post("/api/rce", {
            lang: this.language,
            code: editor.getValue(),
          })
          .then((result) => {
            const {
              data: { exitcode, stdout, stderr },
            } = result;
            this.executionResult = ExecutionResult.success(exitcode, stdout, stderr);
          })
          .catch((e) => {
            console.error(e);
            this.executionResult = ExecutionResult.failure();
          });
      },

      async getDescription() {
        this.descriptionResult = DescriptionResult.loading();
        await axios
          .get(`/api/describe/${this.language}`)
          .then((result) => {
            const {
              data: { description, ubuntu, packages },
            } = result;
            this.descriptionResult = DescriptionResult.success(
              description,
              `Ubuntu ${ubuntu}`,
              packages
            );
          })
          .catch((e) => {
            console.error(e);
            this.descriptionResult = DescriptionResult.failure();
          });
      },

      changeLanguage() {
        LANGUAGE_TEMPLATES[this.lastLanguage] = editor.getValue();
        editor.setValue(LANGUAGE_TEMPLATES[this.language]);
        monaco.editor.setModelLanguage(editor.getModel(), this.language);
        this.lastLanguage = this.language;
      },
    },
  });