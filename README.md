<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="description"
        content="RAM: Towards an Ever-Improving Memory System by Learning from Communications.">
  <meta name="keywords" content="RAG, CL, RLHF">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RAM: Towards an Ever-Improving Memory System by Learning from Communications</title>

  <!-- Global site tag (gtag.js) - Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-PYVRSFMDRL"></script>
  <script>
    window.dataLayer = window.dataLayer || [];

    function gtag() {
      dataLayer.push(arguments);
    }

    gtag('js', new Date());

    gtag('config', 'G-PYVRSFMDRL');
  </script>

  <link href="https://fonts.googleapis.com/css?family=Google+Sans|Noto+Sans|Castoro"
        rel="stylesheet">

  <link rel="stylesheet" href="./static/css/bulma.min.css">
  <link rel="stylesheet" href="./static/css/bulma-carousel.min.css">
  <link rel="stylesheet" href="./static/css/bulma-slider.min.css">
  <link rel="stylesheet" href="./static/css/fontawesome.all.min.css">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
  <link rel="stylesheet" href="./static/css/index.css">
<!--  <link rel="icon" href="./static/images/favicon.svg">-->

  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script defer src="./static/js/fontawesome.all.min.js"></script>
  <script src="./static/js/bulma-carousel.min.js"></script>
  <script src="./static/js/bulma-slider.min.js"></script>
  <script src="./static/js/index.js"></script>
  <script type="text/javascript" async
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
  </script>
</head>
<body>


<section class="hero">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <div class="columns is-centered">
        <div class="column has-text-centered">
          <h1 class="title is-1 publication-title">RAM: Towards an Ever-Improving Memory System by Learning from Communications</h1>
          <div class="is-size-5 publication-authors">
            <span class="author-block">
              <a href="#">Jiaqi Li</a>,</span>
            <span class="author-block">
              <a href="#">Xiaobo Wang</a>,</span>
            <span class="author-block">
              <a href="#">Zihao Wang</a>,</span>
            <span class="author-block">
              <a href="#">Zilong Zheng</a>,</span>
          </div>

          <div class="is-size-5 publication-authors">
            <span class="author-block">Beijing Institute for General Artificial Intelligence (BIGAI), Beijing, China</span>
          </div>

          <div class="column has-text-centered">
            <div class="publication-links">
              <!-- PDF Link. -->
              <span class="link-block">
                <a href="https://arxiv.org/pdf/2404.12045.pdf"
                   class="external-link button is-normal is-rounded is-dark">
                  <span class="icon">
                      <i class="fas fa-file-pdf"></i>
                  </span>
                  <span>Paper</span>
                </a>
              </span>
              <span class="link-block">
                <a href="https://arxiv.org/abs/2404.12045"
                   class="external-link button is-normal is-rounded is-dark">
                  <span class="icon">
                      <i class="ai ai-arxiv"></i>
                  </span>
                  <span>arXiv</span>
                </a>
              </span>
              <!-- Code Link. -->
              <span class="link-block">
                <a href="https://github.com/bigai-nlco/RAM"
                   class="external-link button is-normal is-rounded is-dark">
                  <span class="icon">
                      <i class="fab fa-github"></i>
                  </span>
                  <span>Code</span>
                  </a>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="hero teaser">
  <div class="container is-max-desktop">
    <div class="hero-body">
      <h2 class="subtitle has-text-centered">
        <span class="dnerf">Ram</span>, an innovative RAG-based framework with an ever-improving memory, demonstrating significant improvements over traditional RAG and self-knowledge methods, particularly excelling in handling false premise and multi-hop questions.
      </h2>
      <img src="static/images/framework.png">
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    <!-- Abstract. -->
    <div class="columns is-centered has-text-centered">
      <div class="column is-four-fifths">
        <h2 class="title is-3">Abstract</h2>
        <div class="content has-text-justified">
          We introduce <b>RAM</b>, an innovative RAG-based framework with an ever-improving memory. Inspired by humans' pedagogical process, RAM utilizes recursively reasoning-based retrieval and experience reflections to continually update the memory and learn from users' communicative feedback, namely communicative learning.
 Extensive experiments with both simulated and real users demonstrate significant improvements over traditional RAG and self-knowledge methods, particularly excelling in handling false premise and multi-hop questions.
 Furthermore, RAM exhibits promising adaptability to various feedback and retrieval methods, showcasing its potential for advancing AI capabilities in dynamic knowledge acquisition and lifelong learning.
        </div>
      </div>
    </div>
    <!--/ Abstract. -->
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    <div class="columns is-centered">
      <div class="column is-full-width">
        <h2 class="title is-3">The Framework of RAM</h2>
        <div class="content has-text-justified">
          <p>
          <span style="color: red"><b>RAM</b></span> is a innovative framework that contains three key components, and they can collaborate to work together. More detailed information about these components is as follows:
          </p>
          <ul>
            <li><b>R<sup>3</sup>: <u>R</u>ecursive <u>R</u>easoning-based <u>R</u>etrieval</b>  In this paper, we employ ReAct as the reasoning strategy to choose steps of thought, action, and observation. We replace the lookup/search action in the original ReAct using RAG from the existing memory with limited knowledge. After each trial, the model utilizes self-reflection to learn from previous scratchpads. </li>
            <li><b>An Ever-Improving Memory</b>  We build an ever-improving memory by collecting inferences and feedback in all the trials as context and prompting the LLM with the ground truth to generate a reflected memory. Then we update the memory by utilizing the semantic similarity to localize the most relevant memory piece and replacing the memory piece as the reflected memory. </li>
            <li><b>Knowledge From Human Feedback</b>  Interactively learning from feedback is crucial for agents to avoid repeated errors from historical trials and accelerate the learning process with limited knowledge and capabilities. We describe three different categories of human feedback in RAM as below.
              <ul>
                <li><b>Feedback without explanation</b>  It serves as an automatic evaluator for inference in trails for further retrieval and self-reflection. </li>
                <li><b>Feedback with hints</b>  Instead of offering ground truth directly (or statements semantically the same), it not only allows the model to learn the association among multiple relevant pieces of knowledge in a single problem but also teaches the model the way of thinking to continually promote its intricate reasoning capability from historical trials. </li>
                <li><b>Feedback with direct answers</b>  Feedback with ground truth retrievals can provide clear and explicit correct responses. It is more efficient to expedite the learning process and eliminate ambiguity from being caught in a dilemma after several rounds of recursive thinking and actions. </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    <div class="columns is-centered">
      <div class="column is-full-width">
        <h2 class="title is-3">Experiment Setting</h2>
        <div class="content has-text-justified">
          <ul>
            <li><b>Dataset & Preprocessing</b>  We evaluate the performance of \model with two QA datasets: FreshQA and MQuAKE-T, both of which are newly constructed and mostly contain the latest knowledge in 2023 to avoid data leakage. </li>
            <li><b>Backbone</b>  We mainly use LLaMA-2-7B as the backbone for all experiments. </li>
            <li><b>Evaluation metrics</b>  For each dataset, we follow \citet{baktash2023gpt4} to use <b>GPT4_score</b> and the semantic similarity based <b>BERTScore</b> as the major evaluation metric widely used for open-domain question answering. To further assess the relative performance variations under different settings, we adopt automatic metrics <b>True Positive Rate (TPR)</b>, <b>False Negative Rate (FNR)</b>. </li>
            <li><b>User Simulation</b>  We ran a small-scale experiment with real users to test whether users could, in practice, improve the system's performance. Specifically, we sampled 30 questions that the model struggled with in various categories and multi-hops from the two datasets to keep the variance for testing. 16 users with a minimum undergraduate degree were asked to participate as human teachers in RAM. On average, users provided 2 feedback per question, and the completion time was 2.5 hours. </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    <div class="columns is-centered">
      <div class="column is-full-width">
        <h2 class="title is-3">Results and Analysis</h2>
        <div class="columns is-vcentered interpolation-panel">
        </div>
        <br/>
        <div class="content has-text-justified">
          <h3 class="title is-4">Main Results</h3>
          We measure the model's ability to answer fresh questions under five retrieval-based methods:
          <ul>
            <li><span style="color: red"><b>Self-knowledge:</b></span> directly answering the questions with pre-trained self-knowledge; </li>
            <li><span style="color: red"><b>RAG-only:</b></span> answering the questions based on retrieval from old memory; </li>
            <li><span style="color: red"><b>RAM-R<sup>3</sup>:</b></span> answering the questions only using R<sup>3</sup> based on \(M^{old}\); </li>
            <li><span style="color: red"><b>RAM:</b></span> answering each question using RAM process to obtain \(M^{cur}\). We use ``Feedback with hints'' to provide simulated human feedback. We fix the order of questions to produce consistent memory update results; </li>
            <li><span style="color: red"><b>RAG-upd(RAG with updated memory):</b></span> using the direct answer as feedback for all learning traces and providing RAG-only results based on \(M^{upd}\) with the latest knowledge. The average similarity between \(m^{R}\) with the ground truth of each question is 0.95(FreshQA) and 0.91(MQuAKE) indicating that the memory contains all knowledge of corresponding questions learned from RAM. </li>
          </ul>
          <div align="center">
            <img src="static/images/main_result.png" alt="main results" width="500px">
          </div>
        </div>
        <div class="content has-text-justified">
          <h3 class="title is-4">Analysis</h3>
          <img src="static/images/more_results.png" alt="more results">
          <h4 class="title is-8">(a) Evaluation on various categories of questions in FreshQA</h4>
            <ul>
              <li>RAM benefits largely when answering false premise questions: RAM significantly contributes to the false premise questions (over 40% accuracy improvements) and shows impressive performance above RAG-upd, even when the ground truth is in the memory. </li>
              <li>RAM boosts the learning of slow/never-changing knowledge: RAM especially promotes the learning of slow-changing and never-changing questions to a large extent. It is mainly because the recent knowledge in these two categories probably has close associations with existing memory and can be further deduced through multi-hop reasoning or computations. </li>
            </ul>
          <h4 class="title is-8">(b) Effect of the ever-improving memory in RAM</h4>
          <p>RAG-rel and RAM-rel increase their performance respectively by leveraging the additional knowledge from  \(M^{upd}\) in historical trials. </p>
          <h4 class="title is-8">(c) Performance using feedback with hints and direct answers</h4>
          <p>The average text similarity between both settings is extremely low showing their discrepancy. RAM with hints yields a +8% and +20% higher accuracy than the other in each dataset respectively. Relevant knowledge in hints (although it is not the exact ground truth to any other question) provides further gains across questions that have implicitly shared knowledge. </p>
          <h4 class="title is-8">(d) Accuracy evaluated by real users with interaction</h4>
          <p>Divergent content and methodologies of feedback have a great influence on the effectiveness of learning from communications, which needs to be further explored in future works. </p>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section" id="BibTeX">
  <div class="container is-max-desktop content">
    <h2 class="title">BibTeX</h2>
    <pre><code>@article{li2024ram,
      title={RAM: Towards an Ever-Improving Memory System by Learning from Communications},
      author={Jiaqi Li and Xiaobo Wang and Zihao Wang and Zilong Zheng},
      year={2024},
      eprint={2404.12045},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}</code></pre>
  </div>
</section>


<footer class="footer">
  <div class="container">
    <div class="content has-text-centered">
      <a class="icon-link"
         href=#>
        <i class="fas fa-file-pdf"></i>
      </a>
      <a class="icon-link" href="https://github.com/bigai-nlco/RAM" class="external-link" disabled>
        <i class="fab fa-github"></i>
      </a>
    </div>
    <div class="columns is-centered">
      <div class="column is-8">
        <div class="content">
          <p>
            This website is licensed under a <a rel="license"
                                                href="http://creativecommons.org/licenses/by-sa/4.0/">Creative
            Commons Attribution-ShareAlike 4.0 International License</a>.
          </p>
          <p>
            This means you are free to borrow the <a
              href="https://github.com/nerfies/nerfies.github.io">source code</a> of this website,
            we just ask that you link back to this page in the footer.
            Please remember to remove the analytics code included in the header of the website which
            you do not want on your website.
          </p>
        </div>
      </div>
    </div>
  </div>
</footer>

</body>
</html>
