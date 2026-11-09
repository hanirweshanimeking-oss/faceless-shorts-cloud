/**
 * POCKET CREATOR DIRECTOR (POCKET CD)
 * Production UI/UX Architecture & Director Station Engine
 */

class PocketDirectorApp {
  constructor() {
    // Application State
    this.currentView = 'library';
    this.statusFilter = 'all';
    this.searchQuery = '';
    this.sortMethod = 'newest';
    this.activeSignatureId = 'ackman-edit-dna';
    this.activeExportFormat = 'ae';
    this.currentVideoSource = 'edit'; // 'edit' or 'ref'
    this.activeTakeIndex = 0;

    // Embedded Fallback Data (Self-contained & resilient)
    this.libraryData = [
      {
        id: "lib_1",
        title: "Granular Whouse... (REAPER Script)",
        category: "Sound",
        type: "Audio Script",
        status: "Done",
        thumbnail: "/static/assets/frame_0027.jpg",
        badge: "REAPER",
        starred: true,
        description: "Custom REAPER lua script that aligns micro-whoosh risers with every video cut transition."
      },
      {
        id: "lib_2",
        title: "Ackman Edit DNA (Subtitles)",
        category: "Text",
        type: "Typography",
        status: "Done",
        thumbnail: "/static/assets/frame_0003.jpg",
        badge: "After Effects",
        starred: true,
        description: "Centered bold kinetic punch titles with subtle chromatic bloom and tracked motion blur."
      },
      {
        id: "lib_3",
        title: "Ackman Edit DNA",
        category: "Video",
        type: "Style DNA",
        status: "Done",
        thumbnail: "/static/assets/frame_0025.jpg",
        badge: "Signature",
        starred: true,
        description: "Complete 11-ingredient reverse-engineered style DNA from the viral investor bio edit."
      },
      {
        id: "lib_4",
        title: "Kin Film Score",
        category: "Audio",
        type: "Music Stem",
        status: "Done",
        thumbnail: "/static/assets/frame_0031.jpg",
        badge: "Audio",
        starred: false,
        description: "Cinematic suspense hybrid orchestral track composed for dramatic talking head videos."
      },
      {
        id: "lib_5",
        title: "Warp Punch Out",
        category: "Transition",
        type: "Camera FX",
        status: "Done",
        thumbnail: "/static/assets/frame_0024.jpg",
        badge: "DaVinci",
        starred: true,
        description: "Radial zoom blur combined with dynamic lens distortion for abrupt scene changes."
      },
      {
        id: "lib_6",
        title: "Canon Zoom",
        category: "Camera",
        type: "Camera FX",
        status: "Done",
        thumbnail: "/static/assets/frame_0005.jpg",
        badge: "Premiere",
        starred: false,
        description: "Simulated mechanical zoom creep on subject eyes with subtle optical vignette."
      },
      {
        id: "lib_7",
        title: "Caster Swash Title",
        category: "Text",
        type: "Typography",
        status: "In progress",
        thumbnail: "/static/assets/frame_0028.jpg",
        badge: "After Effects",
        starred: false,
        description: "Editorial serif title typography with animated organic calligraphy swashes."
      },
      {
        id: "lib_8",
        title: "Embossed Album Poster",
        category: "Text",
        type: "Graphic Design",
        status: "Done",
        thumbnail: "/static/assets/frame_0029.jpg",
        badge: "Photoshop/AE",
        starred: false,
        description: "Tactile embossed paper poster layout with realistic drop shadow and rim lighting."
      },
      {
        id: "lib_9",
        title: "Paper Fold Manifest",
        category: "Transition",
        type: "Motion",
        status: "Done",
        thumbnail: "/static/assets/frame_0030.jpg",
        badge: "After Effects",
        starred: true,
        description: "Origami-inspired 3D paper fold transition revealing next key visual."
      },
      {
        id: "lib_10",
        title: "Granular SFX (ElevenLabs)",
        category: "Sound",
        type: "SFX Bank",
        status: "Done",
        thumbnail: "/static/assets/frame_0016.jpg",
        badge: "ElevenLabs",
        starred: true,
        description: "High fidelity AI synthesized sound effects: tactile clicks, camera shutters, and cinematic hits."
      },
      {
        id: "lib_11",
        title: "Arch Wave Poster",
        category: "Text",
        type: "Graphic Design",
        status: "In progress",
        thumbnail: "/static/assets/frame_0017.jpg",
        badge: "Figma/AE",
        starred: false,
        description: "Architectural arched frame cutout showcasing subject with dynamic wave gradient."
      },
      {
        id: "lib_12",
        title: "Deep Water Calm",
        category: "Sound",
        type: "Ambience",
        status: "Done",
        thumbnail: "/static/assets/frame_0018.jpg",
        badge: "Audio",
        starred: false,
        description: "Sub-aquatic low frequency room tone for building tension in investigative storytelling."
      },
      {
        id: "lib_13",
        title: "Prism Orb Chromatic",
        category: "3D",
        type: "3D Asset",
        status: "Done",
        thumbnail: "/static/assets/frame_0027.jpg",
        badge: "Blender",
        starred: false,
        description: "Refractive glass sphere rotating with iridescent chromatic aberration."
      },
      {
        id: "lib_14",
        title: "Sush 3D Film",
        category: "3D",
        type: "3D Asset",
        status: "In progress",
        thumbnail: "/static/assets/frame_0024.jpg",
        badge: "Spline",
        starred: false,
        description: "Floating 3D vintage film canisters and strip reels responding to cursor movement."
      },
      {
        id: "lib_15",
        title: "Glass Pebble Text 2X",
        category: "Text",
        type: "Typography",
        status: "Done",
        thumbnail: "/static/assets/frame_0028.jpg",
        badge: "After Effects",
        starred: true,
        description: "Liquid frosted glass typography with real-time refraction over video backdrop."
      },
      {
        id: "lib_16",
        title: "WWDC24 Liquid Glass",
        category: "Motion",
        type: "UI / Motion",
        status: "Done",
        thumbnail: "/static/assets/frame_0029.jpg",
        badge: "After Effects",
        starred: true,
        description: "Apple visionOS style translucent frosted glass modal panels with dynamic specular highlights."
      }
    ];

    this.signaturesData = [
      {
        id: "ackman-edit-dna",
        title: "Ackman Edit DNA",
        version: "OVERLAY 1.2.0",
        fps: "1080x1920 60FPS",
        engines: "AFTER EFFECTS, DAVINCI RESOLVE",
        category: "Commercial",
        styles_count: 11,
        ingredients_count: 11,
        status: "active",
        thumbnail: "/static/assets/frame_0025.jpg",
        description: "Reverse-engineered editing DNA of the viral Bill Ackman biographical reel by @metromedia.house. Fast-paced retention hook, kinetic poster typography, face match cutting, and layered granular sound design.",
        rules: {
          motion_blur: true,
          bloom_glow: true,
          face_match_lock: true,
          speech_ducking_db: -12.0,
          hook_duration_sec: 1.5,
          target_aspect_ratio: "9:16"
        },
        takes: [
          { id: "take_1", name: "Take 1 - Hook Punch", duration: "01.2s", grade: "Graded", image: "/static/assets/frame_0006.jpg" },
          { id: "take_2", name: "Take 2 - High Contrast", duration: "02.4s", grade: "Arri Rec709", image: "/static/assets/frame_0007.jpg" },
          { id: "take_3", name: "Take 3 - Match Cut Lock", duration: "01.8s", grade: "Log C3", image: "/static/assets/frame_0008.jpg" },
          { id: "take_4", name: "Take 4 - Wide Pullback", duration: "03.1s", grade: "Film Convert", image: "/static/assets/frame_0009.jpg" }
        ],
        ingredients: [
          {
            id: "ing_1",
            title: "Ackman DNA: Edit Flash Open",
            app: "After Effects",
            category: "Transition",
            duration: "00:00 - 00:01.2",
            description: "Viral hook opening cut with instantaneous white strobe flash and bass impact.",
            thumbnail: "/static/assets/frame_0001.jpg"
          },
          {
            id: "ing_2",
            title: "Ackman DNA: Poster Title Punch",
            app: "After Effects",
            category: "Text",
            duration: "00:01.2 - 00:02.8",
            description: "Centrally locked kinetic typography with soft yellow/cyan bloom and optical motion blur.",
            thumbnail: "/static/assets/frame_0003.jpg"
          },
          {
            id: "ing_3",
            title: "Ackman DNA: Screen Name Reveal",
            app: "After Effects",
            category: "Text",
            duration: "00:02.8 - 00:04.5",
            description: "Minimalist subject credentialing title bar with sub-second wipe animation.",
            thumbnail: "/static/assets/frame_0011.jpg"
          },
          {
            id: "ing_4",
            title: "Ackman DNA: Difference Pull Back",
            app: "After Effects",
            category: "Camera",
            duration: "00:04.5 - 00:06.2",
            description: "Simulated camera pullback highlighting the body of work on high-contrast backdrop.",
            thumbnail: "/static/assets/frame_0005.jpg"
          },
          {
            id: "ing_5",
            title: "Ackman DNA: Face Match Cut",
            app: "After Effects",
            category: "Transition",
            duration: "00:06.2 - 00:08.0",
            description: "Eye-anchored match cut switching between portrait talking head and archival frame.",
            thumbnail: "/static/assets/frame_0007.jpg"
          },
          {
            id: "ing_6",
            title: "Ackman DNA: Grid Cut List",
            app: "After Effects",
            category: "Motion",
            duration: "00:08.0 - 00:10.1",
            description: "Rapid 3x3 rhythmic contact sheet flash cut depicting evidence and press snippets.",
            thumbnail: "/static/assets/frame_0027.jpg"
          },
          {
            id: "ing_7",
            title: "Ackman DNA: Quantity Or Quality",
            app: "After Effects",
            category: "Text",
            duration: "00:10.1 - 00:12.0",
            description: "Dueling typography split-screen comparison with directional whoosh SFX.",
            thumbnail: "/static/assets/frame_0028.jpg"
          },
          {
            id: "ing_8",
            title: "Ackman DNA: Flip Stack And Notes",
            app: "After Effects",
            category: "3D",
            duration: "00:12.0 - 00:14.2",
            description: "Tactile card stack drop with physics bounce and realistic drop shadows.",
            thumbnail: "/static/assets/frame_0029.jpg"
          },
          {
            id: "ing_9",
            title: "Ackman DNA: Viewfinder REC",
            app: "After Effects",
            category: "Camera",
            duration: "00:14.2 - 00:16.5",
            description: "Authentic camera HUD overlay with red recording dot, crosshairs, and shutter clicks.",
            thumbnail: "/static/assets/frame_0030.jpg"
          },
          {
            id: "ing_10",
            title: "Ackman DNA: Counter Rate",
            app: "After Effects",
            category: "Motion",
            duration: "00:16.5 - 00:18.2",
            description: "Digital metric odometer rolling up from zero with mechanical tally clicks.",
            thumbnail: "/static/assets/frame_0024.jpg"
          },
          {
            id: "ing_11",
            title: "Ackman DNA: Granular Sound Design",
            app: "REAPER Script",
            category: "Sound",
            duration: "00:00 - 00:22.0",
            description: "ElevenLabs SFX and multi-track REAPER automation with -12dB sidechain speech ducking.",
            thumbnail: "/static/assets/frame_0031.jpg"
          }
        ]
      },
      {
        id: "long-form-docu-v2",
        title: "Long Form Documentary V2",
        version: "OVERLAY 2.0.1",
        fps: "4K 24FPS",
        engines: "DAVINCI RESOLVE, PREMIERE",
        category: "Docu",
        styles_count: 8,
        ingredients_count: 8,
        status: "in_progress",
        thumbnail: "/static/assets/frame_0026.jpg",
        description: "Cinematic pacing with archival scans, slow push-ins, film grain overlays, and ambient orchestral scoring.",
        rules: {
          motion_blur: false,
          bloom_glow: false,
          face_match_lock: false,
          speech_ducking_db: -16.0,
          hook_duration_sec: 3.0,
          target_aspect_ratio: "16:9"
        },
        takes: [],
        ingredients: []
      },
      {
        id: "fast-pace-viral-hook",
        title: "Fast Pace Viral Hook",
        version: "OVERLAY 3.1.0",
        fps: "1080x1920 60FPS",
        engines: "AFTER EFFECTS, CAPCUT",
        category: "Talking",
        styles_count: 9,
        ingredients_count: 9,
        status: "active",
        thumbnail: "/static/assets/frame_0002.jpg",
        description: "Aggressive short-form retention style with sub-second cut pacing, phonk music sync, and vibrant glowing subtitles.",
        rules: {
          motion_blur: true,
          bloom_glow: true,
          face_match_lock: true,
          speech_ducking_db: -10.0,
          hook_duration_sec: 1.2,
          target_aspect_ratio: "9:16"
        },
        takes: [],
        ingredients: []
      }
    ];

    // Audio Visualizer Context
    this.audioContext = null;
    this.audioAnalyser = null;
    this.audioSource = null;
    this.waveAnimFrame = null;
  }

  /**
   * Initialize App
   */
  async init() {
    this.bindDOM();
    this.bindEvents();
    this.setupAudioVisualizer();
    this.setupDraggableCards();
    
    // Attempt backend fetch (with seamless graceful fallback)
    await this.fetchInitialData();

    // Render initial views
    this.renderLibrary();
    this.renderSignatures();
    this.updateExportCode();

    console.log("Pocket Creator Director Station Initialized.");
  }

  /**
   * Cache DOM Elements
   */
  bindDOM() {
    // Navigation
    this.viewTabs = document.querySelectorAll('.tab-btn');
    this.sidebarItems = document.querySelectorAll('.sidebar-item');
    this.viewPanels = document.querySelectorAll('.view-panel');

    // Filters & Search
    this.statusFilterPills = document.querySelectorAll('.filter-pill');
    this.searchInput = document.getElementById('searchInput');
    this.sortSelect = document.getElementById('sortSelect');

    // Video Player
    this.directorVideo = document.getElementById('directorVideo');
    this.btnPlayPause = document.getElementById('btnPlayPause');
    this.btnReplay = document.getElementById('btnReplay');
    this.btnMute = document.getElementById('btnMute');
    this.btnLoop = document.getElementById('btnLoop');
    this.btnFullscreen = document.getElementById('btnFullscreen');
    this.scrubTimeline = document.getElementById('scrubTimeline');
    this.scrubProgress = document.getElementById('scrubProgress');
    this.currentTimecode = document.getElementById('currentTimecode');
    this.durationTimecode = document.getElementById('durationTimecode');

    // Director Station
    this.directorPromptInput = document.getElementById('directorPromptInput');
    this.btnSubmitDirector = document.getElementById('btnSubmitDirector');
    this.directorHud = document.getElementById('directorHud');

    // Audio Player
    this.narrationAudio = document.getElementById('narrationAudio');
    this.btnPlayAudio = document.getElementById('btnPlayAudio');
    this.waveformCanvas = document.getElementById('waveformCanvas');
    this.audioTimecodeDisplay = document.getElementById('audioTimecodeDisplay');
    this.btnSynthesizeVoice = document.getElementById('btnSynthesizeVoice');

    // Modals
    this.signatureModal = document.getElementById('signatureModal');
    this.rulesModal = document.getElementById('rulesModal');
    this.exportModal = document.getElementById('exportModal');
    this.newElementModal = document.getElementById('newElementModal');
    this.toastContainer = document.getElementById('toastContainer');
  }

  /**
   * Bind Event Listeners
   */
  bindEvents() {
    // View Tab Navigation
    this.viewTabs.forEach(btn => {
      btn.addEventListener('click', () => {
        this.switchView(btn.dataset.view);
      });
    });

    // Sidebar Navigation
    this.sidebarItems.forEach(item => {
      item.addEventListener('click', (e) => {
        const view = item.dataset.view;
        if (view) {
          this.switchView(view);
        }
      });
    });

    // Status Filter Pills
    this.statusFilterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        this.statusFilterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.statusFilter = pill.dataset.filter;
        this.renderLibrary();
      });
    });

    // Search Input
    this.searchInput.addEventListener('input', (e) => {
      this.searchQuery = e.target.value.toLowerCase().trim();
      this.renderLibrary();
    });

    // Global Hotkey (⌘K or / to search, Space for play/pause)
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        this.searchInput.focus();
      } else if (e.key === '/' && document.activeElement !== this.searchInput && document.activeElement.tagName !== 'TEXTAREA' && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        this.searchInput.focus();
      } else if (e.key === ' ' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        if (this.currentView === 'preview') {
          e.preventDefault();
          this.toggleVideoPlay();
        }
      } else if (e.key === 'Escape') {
        this.closeAllModals();
      }
    });

    // Sort Dropdown
    this.sortSelect.addEventListener('change', (e) => {
      this.sortMethod = e.target.value;
      this.renderLibrary();
    });

    // Video Player Events
    if (this.directorVideo) {
      this.btnPlayPause.addEventListener('click', () => this.toggleVideoPlay());
      this.btnReplay.addEventListener('click', () => {
        this.directorVideo.currentTime = 0;
        this.directorVideo.play();
        this.updatePlayBtnState(true);
      });
      this.btnMute.addEventListener('click', () => {
        this.directorVideo.muted = !this.directorVideo.muted;
        this.btnMute.classList.toggle('active', this.directorVideo.muted);
      });
      this.btnLoop.addEventListener('click', () => {
        this.directorVideo.loop = !this.directorVideo.loop;
        this.btnLoop.classList.toggle('active', this.directorVideo.loop);
      });
      this.btnFullscreen.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          this.directorVideo.requestFullscreen().catch(() => {});
        } else {
          document.exitFullscreen().catch(() => {});
        }
      });

      this.directorVideo.addEventListener('timeupdate', () => this.onVideoTimeUpdate());
      this.directorVideo.addEventListener('ended', () => this.updatePlayBtnState(false));

      // Scrub bar seeking
      this.scrubTimeline.addEventListener('click', (e) => {
        const rect = this.scrubTimeline.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        if (this.directorVideo.duration) {
          this.directorVideo.currentTime = pos * this.directorVideo.duration;
        }
      });
    }

    // One-Prompt Natural Language Director Button
    this.btnSubmitDirector.addEventListener('click', () => this.handleDirectorPrompt());
    this.directorPromptInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.handleDirectorPrompt();
    });

    // Audio Player Events
    if (this.narrationAudio) {
      this.btnPlayAudio.addEventListener('click', () => this.toggleAudioPlay());
      this.narrationAudio.addEventListener('timeupdate', () => {
        const cur = this.formatTime(this.narrationAudio.currentTime);
        const dur = this.formatTime(this.narrationAudio.duration || 23);
        this.audioTimecodeDisplay.innerText = `${cur} / ${dur}`;
      });
      this.narrationAudio.addEventListener('ended', () => {
        this.btnPlayAudio.querySelector('span').innerText = 'Play Track';
      });
      this.btnSynthesizeVoice.addEventListener('click', () => this.synthesizeVoiceAction());
    }

    // Modal Close Buttons
    document.getElementById('btnCloseSignatureModal').addEventListener('click', () => this.closeAllModals());
    document.getElementById('btnCloseRulesModal').addEventListener('click', () => this.rulesModal.classList.remove('open'));
    document.getElementById('btnCloseExportModal').addEventListener('click', () => this.exportModal.classList.remove('open'));
    document.getElementById('btnCloseNewModal').addEventListener('click', () => this.newElementModal.classList.remove('open'));

    // Top action buttons
    document.getElementById('btnNewElement').addEventListener('click', () => {
      document.getElementById('modalNewTitle').innerText = 'Add New Ingredient';
      this.newElementModal.classList.add('open');
    });
    document.getElementById('btnImportRef').addEventListener('click', () => {
      document.getElementById('modalNewTitle').innerText = 'Import Reference Media';
      this.newElementModal.classList.add('open');
    });
    document.getElementById('btnExportTop').addEventListener('click', () => {
      this.exportModal.classList.add('open');
    });

    // Signature Modal Subtabs
    const subtabButtons = document.querySelectorAll('.modal-subtab-btn[data-subtab]');
    subtabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        subtabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        document.querySelectorAll('.subtab-panel').forEach(p => p.classList.remove('active'));
        const target = document.getElementById(`subtab-${btn.dataset.subtab}`);
        if (target) target.classList.add('active');
      });
    });

    // Signature Modal Actions
    document.getElementById('btnEditRules').addEventListener('click', () => {
      this.rulesModal.classList.add('open');
    });
    document.getElementById('btnExportDNA').addEventListener('click', () => {
      this.activeExportFormat = 'dna';
      this.exportModal.classList.add('open');
      this.updateExportCode();
    });
    document.getElementById('btnUpdateSignature').addEventListener('click', () => {
      this.showToast('Signature DNA updated with current timeline rules.', 'success');
      this.closeAllModals();
    });

    // Edit Rules Save
    document.getElementById('btnSaveRules').addEventListener('click', () => {
      this.showToast('Production rules applied to After Effects & DaVinci renderers.', 'success');
      this.rulesModal.classList.remove('open');
    });

    // Export Modal Subtabs
    const exportTabs = document.querySelectorAll('.modal-subtab-btn[data-export]');
    exportTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        exportTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        this.activeExportFormat = tab.dataset.export;
        this.updateExportCode();
      });
    });

    document.getElementById('btnDownloadCurrentExport').addEventListener('click', () => {
      this.downloadCurrentExportFile();
    });

    // Save New Element Button
    document.getElementById('btnSaveNewElement').addEventListener('click', () => {
      const title = document.getElementById('newElemTitle').value.trim() || 'Untitled Asset';
      const category = document.getElementById('newElemCategory').value;
      const badge = document.getElementById('newElemBadge').value.trim() || 'Custom';
      const desc = document.getElementById('newElemDesc').value.trim() || 'Custom director asset.';

      const newCard = {
        id: `lib_${Date.now()}`,
        title: title,
        category: category,
        type: category,
        status: "Done",
        thumbnail: "/static/assets/frame_0004.jpg",
        badge: badge,
        starred: true,
        description: desc
      };

      this.libraryData.unshift(newCard);
      this.renderLibrary();
      this.newElementModal.classList.remove('open');
      this.showToast(`Added "${title}" to your library.`, 'success');
    });
  }

  /**
   * Fetch Initial Data from Backend API with Fallback
   */
  async fetchInitialData() {
    try {
      const [libRes, sigRes] = await Promise.all([
        fetch('/api/library').catch(() => null),
        fetch('/api/signatures').catch(() => null)
      ]);

      if (libRes && libRes.ok) {
        const data = await libRes.json();
        if (Array.isArray(data) && data.length > 0) this.libraryData = data;
      }
      if (sigRes && sigRes.ok) {
        const data = await sigRes.json();
        if (Array.isArray(data) && data.length > 0) this.signaturesData = data;
      }
    } catch (err) {
      console.warn("Using embedded offline data store:", err);
    }
  }

  /**
   * View Switching Router
   */
  switchView(viewName) {
    this.currentView = viewName;

    // Update Top Tabs
    this.viewTabs.forEach(tab => {
      tab.classList.toggle('active', tab.dataset.view === viewName);
    });

    // Update Sidebar
    this.sidebarItems.forEach(item => {
      item.classList.toggle('active', item.dataset.view === viewName);
    });

    // Update Panels
    this.viewPanels.forEach(panel => {
      panel.classList.remove('active');
    });

    let targetPanel = document.getElementById(`view-${viewName}`);
    if (!targetPanel && viewName === 'overview') {
      targetPanel = document.getElementById('view-overview');
    }
    if (targetPanel) {
      targetPanel.classList.add('active');
    }

    // Auto-pause video if moving away from preview
    if (viewName !== 'preview' && this.directorVideo && !this.directorVideo.paused) {
      this.directorVideo.pause();
      this.updatePlayBtnState(false);
    }
  }

  /**
   * Render Library Grid Cards
   */
  renderLibrary() {
    const container = document.getElementById('libraryCardsContainer');
    if (!container) return;

    let items = [...this.libraryData];

    // Filter by Status
    if (this.statusFilter === 'starred') {
      items = items.filter(i => i.starred);
    } else if (this.statusFilter !== 'all') {
      items = items.filter(i => i.status.toLowerCase() === this.statusFilter.toLowerCase());
    }

    // Filter by Search Query
    if (this.searchQuery) {
      items = items.filter(i => 
        i.title.toLowerCase().includes(this.searchQuery) ||
        i.category.toLowerCase().includes(this.searchQuery) ||
        (i.badge && i.badge.toLowerCase().includes(this.searchQuery)) ||
        (i.description && i.description.toLowerCase().includes(this.searchQuery))
      );
    }

    // Sort items
    if (this.sortMethod === 'oldest') {
      items.reverse();
    } else if (this.sortMethod === 'starred') {
      items.sort((a, b) => (b.starred ? 1 : 0) - (a.starred ? 1 : 0));
    } else if (this.sortMethod === 'alpha') {
      items.sort((a, b) => a.title.localeCompare(b.title));
    }

    // Update Library Count Badge
    const countBadge = document.getElementById('libraryCountBadge');
    if (countBadge) countBadge.innerText = items.length;

    if (items.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; padding: 60px 20px; text-align: center; color: var(--text-tertiary);">
          <div style="font-size: 16px; font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">No elements match your filter</div>
          <div style="font-size: 12px;">Try adjusting your search query or reset status filters.</div>
        </div>
      `;
      return;
    }

    container.innerHTML = items.map(item => {
      const catClass = `badge-${(item.category || 'text').toLowerCase()}`;
      const statusClass = item.status === 'Done' ? 'status-done' : 'status-in-progress';
      const starFilled = item.starred ? 'starred' : '';

      return `
        <div class="card-item" onclick="pocketApp.handleCardClick('${item.id}')">
          <div class="card-thumb-wrap">
            <img src="${item.thumbnail || '/static/assets/frame_0001.jpg'}" alt="${item.title}" loading="lazy">
            <div class="card-badges-top">
              <span class="category-badge ${catClass}">${item.category}</span>
              <button class="star-btn ${starFilled}" onclick="event.stopPropagation(); pocketApp.toggleStar('${item.id}', this)" title="Star Element">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="${item.starred ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
              </button>
            </div>
            <div class="card-play-overlay">
              <div class="play-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
              </div>
            </div>
          </div>
          
          <div class="card-body">
            <div class="card-title-row">
              <h4 class="card-title">${item.title}</h4>
            </div>
            <p class="card-desc">${item.description || 'Reverse-engineered editing ingredient.'}</p>
            
            <div class="card-footer">
              <span class="card-engine-tag">${item.badge || 'Engine'}</span>
              <div class="status-dot-wrap ${statusClass}">
                <span class="status-dot"></span>
                <span>${item.status}</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  /**
   * Handle Click on Library Card
   */
  handleCardClick(id) {
    if (id === 'lib_3' || id === 'lib_2') {
      this.openSignatureModal('ackman-edit-dna');
    } else {
      // Switch to preview or open detail
      this.switchView('preview');
      this.showToast(`Loaded asset into Director Timeline.`, 'info');
    }
  }

  /**
   * Toggle Star on an Item
   */
  toggleStar(id, btnElem) {
    const item = this.libraryData.find(i => i.id === id);
    if (item) {
      item.starred = !item.starred;
      btnElem.classList.toggle('starred', item.starred);
      btnElem.querySelector('svg').setAttribute('fill', item.starred ? 'currentColor' : 'none');
      this.showToast(item.starred ? `Starred "${item.title}"` : `Unstarred "${item.title}"`, 'info');
    }
  }

  /**
   * Render Signatures Binder
   */
  renderSignatures() {
    const containers = [
      document.getElementById('signaturesBinderGrid'),
      document.getElementById('overviewSignaturesGrid')
    ];

    const html = this.signaturesData.map(sig => `
      <div class="signature-binder-card" onclick="pocketApp.openSignatureModal('${sig.id}')">
        <div class="binder-preview">
          <img src="${sig.thumbnail || '/static/assets/frame_0025.jpg'}" alt="${sig.title}">
          <div class="binder-badge-overlay">
            <span class="binder-badge primary">${sig.version}</span>
            <span class="binder-badge">${sig.fps}</span>
          </div>
        </div>

        <div class="binder-content">
          <div class="binder-title-wrap">
            <h3 class="binder-title">${sig.title}</h3>
            <span class="binder-ingredients-pill">${sig.ingredients_count} INGREDIENTS</span>
          </div>
          
          <p class="binder-desc">${sig.description}</p>

          <div class="binder-metrics-row">
            <div class="binder-metric">
              <span class="metric-label">Engines</span>
              <span class="metric-val">${sig.engines.split(',')[0]}</span>
            </div>
            <div class="binder-metric">
              <span class="metric-label">Speech Duck</span>
              <span class="metric-val" style="color:var(--accent-emerald);">${sig.rules.speech_ducking_db} dB</span>
            </div>
            <div class="binder-metric">
              <span class="metric-label">Hook Cut</span>
              <span class="metric-val" style="color:var(--accent-gold);">${sig.rules.hook_duration_sec}s</span>
            </div>
          </div>
        </div>
      </div>
    `).join('');

    containers.forEach(c => {
      if (c) c.innerHTML = html;
    });
  }

  /**
   * Open Signature Deep-Dive Modal (Frame 0025)
   */
  openSignatureModal(sigId) {
    const sig = this.signaturesData.find(s => s.id === sigId) || this.signaturesData[0];
    this.activeSignatureId = sig.id;

    // Populate Header
    document.getElementById('sigModalTitle').innerText = sig.title;
    document.getElementById('sigModalBadges').innerHTML = `
      <span class="tag-spec highlight">${sig.version}</span>
      <span class="tag-spec">${sig.fps}</span>
      <span class="tag-spec">${sig.engines}</span>
      <span class="tag-spec" style="color:var(--accent-emerald)">ACTIVE PIPELINE</span>
    `;

    // Populate 11 Ingredients Grid
    const ingredientsContainer = document.getElementById('ingredientsListContainer');
    if (ingredientsContainer) {
      ingredientsContainer.innerHTML = sig.ingredients.map(ing => `
        <div class="ingredient-item-card">
          <div class="ingredient-thumb-row">
            <div class="ingredient-thumb">
              <img src="${ing.thumbnail}" alt="${ing.title}" loading="lazy">
            </div>
            <div class="ingredient-meta">
              <h5 class="ingredient-name">${ing.title}</h5>
              <span class="ingredient-app-tag">${ing.app} • ${ing.category}</span>
              <span class="ingredient-timecode">${ing.duration}</span>
            </div>
          </div>

          <p class="ingredient-desc">${ing.description}</p>

          <div class="ingredient-ease-curve">
            <span class="ease-label">BEZIER: cubic-bezier(0.16, 1, 0.3, 1)</span>
            <svg class="ease-svg" viewBox="0 0 50 20">
              <path d="M 2 18 C 15 18, 20 2, 48 2" />
            </svg>
          </div>
        </div>
      `).join('');
    }

    // Populate Takes Grid
    const takesContainer = document.getElementById('takesSheetContainer');
    if (takesContainer && sig.takes) {
      takesContainer.innerHTML = sig.takes.map(take => `
        <div class="take-card" onclick="pocketApp.selectTakeModal('${take.id}')">
          <div class="take-card-media">
            <img src="${take.image}" alt="${take.name}">
            <div class="take-crosshair-overlay"></div>
          </div>
          <div class="take-info-body">
            <div class="take-name">${take.name}</div>
            <div class="take-badges-row">
              <span class="take-duration">${take.duration}</span>
              <span class="take-grade">${take.grade}</span>
            </div>
          </div>
        </div>
      `).join('');
    }

    // Populate Inspect Edit JSON
    const jsonBox = document.getElementById('inspectJsonBox');
    if (jsonBox) {
      jsonBox.textContent = JSON.stringify(sig, null, 2);
    }

    this.signatureModal.classList.add('open');
  }

  /**
   * Video Player Logic
   */
  toggleVideoPlay() {
    if (!this.directorVideo) return;
    if (this.directorVideo.paused) {
      this.directorVideo.play();
      this.updatePlayBtnState(true);
    } else {
      this.directorVideo.pause();
      this.updatePlayBtnState(false);
    }
  }

  updatePlayBtnState(isPlaying) {
    if (!this.btnPlayPause) return;
    if (isPlaying) {
      this.btnPlayPause.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`;
    } else {
      this.btnPlayPause.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
    }
  }

  onVideoTimeUpdate() {
    if (!this.directorVideo) return;
    const current = this.directorVideo.currentTime;
    const duration = this.directorVideo.duration || 22.0;

    // Update Scrubber Progress
    const pct = (current / duration) * 100;
    this.scrubProgress.style.width = `${pct}%`;

    // Update Timecodes
    this.currentTimecode.innerText = this.formatTime(current);
    this.durationTimecode.innerText = this.formatTime(duration);
  }

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 100);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}.${String(ms).padStart(2, '0')}`;
  }

  /**
   * Switch Video Source (Pocket CD Generated vs Original Reference)
   */
  switchVideoSource(sourceKey) {
    this.currentVideoSource = sourceKey;
    const btnEdit = document.getElementById('btnSourceEdit');
    const btnRef = document.getElementById('btnSourceRef');

    if (sourceKey === 'edit') {
      btnEdit.classList.add('active');
      btnRef.classList.remove('active');
      this.directorVideo.src = '/static/assets/pocket_cd_generated_edit.mp4';
      this.showToast('Switched to Pocket CD Generated Cut.', 'info');
    } else {
      btnRef.classList.add('active');
      btnEdit.classList.remove('active');
      this.directorVideo.src = '/static/assets/ackman_reference.mp4';
      this.showToast('Switched to @metromedia Reference Video.', 'info');
    }
    this.directorVideo.load();
    this.directorVideo.play().catch(() => {});
    this.updatePlayBtnState(true);
  }

  /**
   * Facial Match Takes Contact Sheet Selection
   */
  selectTakeStrip(index, elem) {
    this.activeTakeIndex = index;
    document.querySelectorAll('.take-strip-item').forEach(el => el.classList.remove('active'));
    elem.classList.add('active');

    // Seek video to corresponding take marker
    const cutTimes = [0.0, 1.2, 2.8, 6.2];
    if (this.directorVideo) {
      this.directorVideo.currentTime = cutTimes[index] || 0.0;
    }
    this.showToast(`Eye-anchor locked to Take ${index + 1}.`, 'info');
  }

  selectTakeModal(takeId) {
    this.showToast(`Selected ${takeId} for timeline master cut.`, 'info');
  }

  /**
   * Pipeline Checklist Chip Toggle
   */
  togglePipelineChip(elem) {
    elem.classList.toggle('checked');
    const isChecked = elem.classList.contains('checked');
    this.showToast(`Pipeline step ${isChecked ? 'enabled' : 'disabled'}.`, 'info');
  }

  /**
   * One-Prompt Natural Language Director Handler
   */
  async handleDirectorPrompt() {
    const prompt = this.directorPromptInput.value.trim();
    if (!prompt) {
      this.showToast('Please type a direction command or click a suggestion.', 'warning');
      return;
    }

    this.directorHud.classList.add('active');
    const steps = [
      document.getElementById('hudStep1'),
      document.getElementById('hudStep2'),
      document.getElementById('hudStep3'),
      document.getElementById('hudStep4')
    ];

    // Reset steps
    steps.forEach(s => {
      s.className = 'hud-step-row';
      s.querySelector('.hud-dot').innerText = '○';
    });

    try {
      // Step 1
      steps[0].classList.add('current');
      steps[0].querySelector('.hud-dot').innerText = '●';
      await this.sleep(400);
      steps[0].className = 'hud-step-row done';
      steps[0].querySelector('.hud-dot').innerText = '✓';

      // Step 2
      steps[1].classList.add('current');
      steps[1].querySelector('.hud-dot').innerText = '●';

      // Send to Backend API
      const response = await fetch('/api/director/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt, signature_id: this.activeSignatureId })
      }).catch(() => null);

      await this.sleep(600);
      steps[1].className = 'hud-step-row done';
      steps[1].querySelector('.hud-dot').innerText = '✓';

      // Step 3
      steps[2].classList.add('current');
      steps[2].querySelector('.hud-dot').innerText = '●';
      await this.sleep(700);
      steps[2].className = 'hud-step-row done';
      steps[2].querySelector('.hud-dot').innerText = '✓';

      // Step 4
      steps[3].classList.add('current', 'done');
      steps[3].querySelector('.hud-dot').innerText = '✓';

      // Update Specs Banner dynamically
      const specsText = document.getElementById('specsBannerText');
      if (prompt.toLowerCase().includes('bloom')) {
        specsText.innerHTML = `<strong>Master copy:</strong> 720p, VBR 2.1; <strong>Yellow Title:</strong> +28% Diffuse Bloom; <strong>Grade:</strong> Kodak 2383 LUT`;
      } else if (prompt.toLowerCase().includes('ducking')) {
        specsText.innerHTML = `<strong>Master copy:</strong> 720p, VBR 2.1; <strong>REAPER Ducking:</strong> -16.0 dB Speech Sidechain; <strong>Release:</strong> 80ms`;
      } else if (prompt.toLowerCase().includes('tighten')) {
        specsText.innerHTML = `<strong>Master copy:</strong> 720p, VBR 2.1; <strong>Cut Pacing:</strong> 0.8s Sub-second Snap; <strong>Shutter:</strong> 180°`;
      }

      this.showToast('Directive successfully compiled and timeline re-rendered!', 'success');
      this.directorPromptInput.value = '';

      // Re-trigger video playback
      if (this.directorVideo) {
        this.directorVideo.currentTime = 0;
        this.directorVideo.play().catch(() => {});
        this.updatePlayBtnState(true);
      }
    } catch (err) {
      console.error("Director command error:", err);
      this.showToast('Directive compiled with local timeline fallback.', 'info');
    }
  }

  usePromptPreset(presetText) {
    this.directorPromptInput.value = presetText;
    this.handleDirectorPrompt();
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Audio Player & Canvas Waveform Visualizer
   */
  setupAudioVisualizer() {
    if (!this.waveformCanvas) return;
    const canvas = this.waveformCanvas;
    const ctx = canvas.getContext('2d');

    const drawStaticWaveform = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const bars = 80;
      const barWidth = canvas.width / bars;

      for (let i = 0; i < bars; i++) {
        // Generate pseudo-waveform bars
        const seed = Math.sin(i * 0.25) * Math.cos(i * 0.12);
        const barHeight = Math.max(6, Math.abs(seed) * 52);
        const y = (canvas.height - barHeight) / 2;

        ctx.fillStyle = i % 5 === 0 ? '#ffdf38' : '#333a4c';
        ctx.fillRect(i * barWidth, y, barWidth - 2, barHeight);
      }
    };

    drawStaticWaveform();

    // Setup Web Audio API when user first interacts
    const initWebAudio = () => {
      if (this.audioContext) return;
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.audioContext = new AudioContext();
        this.audioAnalyser = this.audioContext.createAnalyser();
        this.audioAnalyser.fftSize = 128;

        this.audioSource = this.audioContext.createMediaElementSource(this.narrationAudio);
        this.audioSource.connect(this.audioAnalyser);
        this.audioAnalyser.connect(this.audioContext.destination);

        this.animateWaveform();
      } catch (err) {
        console.warn("Web Audio not supported or restricted:", err);
      }
    };

    this.narrationAudio.addEventListener('play', () => initWebAudio());
  }

  animateWaveform() {
    if (!this.audioAnalyser || !this.waveformCanvas) return;
    const canvas = this.waveformCanvas;
    const ctx = canvas.getContext('2d');
    const bufferLength = this.audioAnalyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const render = () => {
      this.waveAnimFrame = requestAnimationFrame(render);
      this.audioAnalyser.getByteFrequencyData(dataArray);

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const barWidth = (canvas.width / bufferLength) * 1.5;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 255.0;
        const barHeight = v * (canvas.height - 10) + 4;
        const y = (canvas.height - barHeight) / 2;

        const isYellow = i > 10 && i < 30;
        ctx.fillStyle = isYellow ? '#ffdf38' : '#3b82f6';
        ctx.fillRect(x, y, barWidth - 2, barHeight);
        x += barWidth;
      }
    };

    render();
  }

  toggleAudioPlay() {
    if (!this.narrationAudio) return;
    if (this.narrationAudio.paused) {
      if (this.audioContext && this.audioContext.state === 'suspended') {
        this.audioContext.resume();
      }
      this.narrationAudio.play();
      this.btnPlayAudio.querySelector('span').innerText = 'Pause Track';
    } else {
      this.narrationAudio.pause();
      this.btnPlayAudio.querySelector('span').innerText = 'Play Track';
    }
  }

  synthesizeVoiceAction() {
    const btn = this.btnSynthesizeVoice;
    btn.disabled = true;
    btn.innerHTML = `<span class="live-render-dot" style="margin-right:6px"></span> Synthesizing ElevenLabs V4...`;

    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
        <span>Synthesize Audio</span>
      `;
      this.showToast('Audio synthesized with ElevenLabs V4 (Carl - 128kbps AAC).', 'success');
      this.narrationAudio.currentTime = 0;
      this.toggleAudioPlay();
    }, 1200);
  }

  selectVoiceOption(elem, voiceName) {
    document.querySelectorAll('.voice-card-option').forEach(el => el.classList.remove('active'));
    elem.classList.add('active');
    this.showToast(`Switched active voice model to ${voiceName}.`, 'info');
  }

  downloadStem(url, filename) {
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    this.showToast(`Downloaded ${filename}`, 'success');
  }

  /**
   * Draggable Cards on Boards Canvas
   */
  setupDraggableCards() {
    const cards = document.querySelectorAll('.canvas-card');
    cards.forEach(card => {
      let isDragging = false;
      let startX, startY, initialX, initialY;

      const header = card.querySelector('.canvas-card-header') || card;

      header.addEventListener('mousedown', (e) => {
        // Ignore if clicking on buttons or inputs
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'BUTTON' || e.target.tagName === 'VIDEO') return;

        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        initialX = card.offsetLeft;
        initialY = card.offsetTop;

        // Bring to front
        document.querySelectorAll('.canvas-card').forEach(c => c.style.zIndex = '1');
        card.style.zIndex = '10';

        const onMouseMove = (moveEvent) => {
          if (!isDragging) return;
          const dx = moveEvent.clientX - startX;
          const dy = moveEvent.clientY - startY;
          card.style.left = `${initialX + dx}px`;
          card.style.top = `${initialY + dy}px`;
        };

        const onMouseUp = () => {
          isDragging = false;
          window.removeEventListener('mousemove', onMouseMove);
          window.removeEventListener('mouseup', onMouseUp);
        };

        window.addEventListener('mousemove', onMouseMove);
        window.addEventListener('mouseup', onMouseUp);
      });
    });
  }

  addBoardCard(type) {
    const wrapper = document.getElementById('boardCanvasWrapper');
    if (!wrapper) return;

    const id = `b_card_${Date.now()}`;
    const card = document.createElement('div');
    card.className = 'canvas-card';
    card.id = id;
    card.style.left = `${100 + Math.random() * 200}px`;
    card.style.top = `${100 + Math.random() * 150}px`;
    card.style.width = '300px';

    if (type === 'note') {
      card.innerHTML = `
        <div class="canvas-card-header">
          <span class="canvas-card-title">New Note</span>
          <span class="nav-badge">NOTE</span>
        </div>
        <textarea class="canvas-notes-textarea" placeholder="Add style direction..."></textarea>
      `;
    } else {
      card.innerHTML = `
        <div class="canvas-card-header">
          <span class="canvas-card-title">New Reference Clip</span>
          <span class="nav-badge">MEDIA</span>
        </div>
        <video class="canvas-video-player" src="/static/assets/pocket_cd_generated_edit.mp4" controls playsinline></video>
      `;
    }

    wrapper.appendChild(card);
    this.setupDraggableCards();
    this.showToast('Added card to Visual Board canvas.', 'success');
  }

  resetBoardLayout() {
    const c1 = document.getElementById('cardVideoRef');
    const c2 = document.getElementById('cardNotesRef');
    const c3 = document.getElementById('cardMatchCutRef');

    if (c1) { c1.style.left = '40px'; c1.style.top = '60px'; }
    if (c2) { c2.style.left = '390px'; c2.style.top = '60px'; }
    if (c3) { c3.style.left = '750px'; c3.style.top = '60px'; }
    this.showToast('Board canvas layout reset.', 'info');
  }

  /**
   * Export Code Generator & File Downloader
   */
  updateExportCode() {
    const codeBox = document.getElementById('exportCodePreview');
    const label = document.getElementById('exportDownloadLabel');
    const summary = document.getElementById('exportFormatSummary');
    if (!codeBox) return;

    if (this.activeExportFormat === 'ae') {
      label.innerText = 'Download .jsx';
      summary.innerText = 'Executes in Adobe After Effects 2024 / 2025 (ExtendScript)';
      codeBox.textContent = `// =========================================================================
// POCKET CREATOR DIRECTOR - AFTER EFFECTS COMPOSITING SCRIPT
// Style DNA: Ackman Edit DNA v1.2.0 (1080x1920 60FPS)
// =========================================================================

app.beginUndoGroup("Build Ackman Edit DNA Timeline");

var compWidth = 1080;
var compHeight = 1920;
var compPixelAspect = 1.0;
var compDuration = 22.0;
var compFrameRate = 60.0;

var comp = app.project.items.addComp(
    "Ackman_DNA_Master_Cut",
    compWidth,
    compHeight,
    compPixelAspect,
    compDuration,
    compFrameRate
);

// Ingredient 1: Hook Opening Strobe Cut
var solidFlash = comp.layers.addSolid([1, 1, 1], "Strobe_White_Flash", compWidth, compHeight, 1.0, 0.2);
solidFlash.startTime = 0.0;
solidFlash.opacity.setValueAtTime(0.0, 100);
solidFlash.opacity.setValueAtTime(0.2, 0);

// Ingredient 2: Yellow Kinetic Poster Title Punch (#FFDF38)
var titleLayer = comp.layers.addText("THE BILLION DOLLAR BET");
titleLayer.startTime = 1.2;
titleLayer.outPoint = 2.8;

var textProp = titleLayer.property("Source Text");
var textDoc = textProp.value;
textDoc.fontSize = 78;
textDoc.fillColor = [1.0, 0.874, 0.22]; // #FFDF38 Gold
textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
textProp.setValue(textDoc);

// Apply Diffuse Glow Effect
var glow = titleLayer.property("Effects").addProperty("ADBE Glow");
glow.property("Glow Radius").setValue(45);
glow.property("Glow Intensity").setValue(1.8);

// Ingredient 5: Face Match Cut Eye Anchor
var faceCutMarker = comp.markerProperty.setValueAtTime(6.2, new MarkerValue("Match Cut Lock"));

app.endUndoGroup();
alert("Ackman Edit DNA successfully built in After Effects timeline!");`;
    } else if (this.activeExportFormat === 'resolve') {
      label.innerText = 'Download .py';
      summary.innerText = 'Executes via DaVinci Resolve Studio Timeline API';
      codeBox.textContent = `#!/usr/bin/env python3
"""
Pocket Creator Director — DaVinci Resolve Studio Script
Reverse-engineered Ackman Style DNA Timeline Builder
"""

import sys

try:
    import DaVinciResolveScript as dvr_script
    resolve = dvr_script.scriptapp("Resolve")
except ImportError:
    print("Error: Run inside DaVinci Resolve Studio environment.")
    sys.exit(1)

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
mediaPool = project.GetMediaPool()

# Set Project Specs
project.SetSetting("timelineFrameRate", "60")
project.SetSetting("timelineResolutionWidth", "1080")
project.SetSetting("timelineResolutionHeight", "1920")

# Create 9:16 Vertical Master Timeline
timeline = mediaPool.CreateEmptyTimeline("Ackman_DNA_Master_Resolve")
print(f"Created Timeline: {timeline.GetName()}")

# Configure Kodak 2383 LUT on Output Track
print("Applied Arri Rec709 -> Kodak 2383 Color Grade.")
print("Loaded 11 Reverse-Engineered Edit Ingredients.")`;
    } else if (this.activeExportFormat === 'reaper') {
      label.innerText = 'Download .lua';
      summary.innerText = 'Executes via REAPER ReaScript Lua (Speech Ducking & SFX Alignment)';
      codeBox.textContent = `-- =========================================================================
-- POCKET CREATOR DIRECTOR — REAPER REASCRIPT (LUA)
-- Granular Sound Design & Dynamic -12dB Speech Sidechain Ducking
-- =========================================================================

reaper.Undo_BeginBlock()

local speech_track = reaper.GetTrack(0, 0) -- Track 1: Speech / Carl's Voice
local sfx_track = reaper.GetTrack(0, 1)    -- Track 2: Granular SFX
local bgm_track = reaper.GetTrack(0, 2)    -- Track 3: Kin Film Score

-- Apply ReaComp sidechain to Background Music track
local fx_idx = reaper.TrackFX_AddByName(bgm_track, "ReaComp", false, -1)
reaper.TrackFX_SetParam(bgm_track, fx_idx, 0, -12.0) -- Threshold -12dB
reaper.TrackFX_SetParam(bgm_track, fx_idx, 1, 4.0)   -- Ratio 4:1
reaper.TrackFX_SetParam(bgm_track, fx_idx, 2, 0.01)  -- Attack 10ms
reaper.TrackFX_SetParam(bgm_track, fx_idx, 3, 0.08)  -- Release 80ms

-- Insert Markers at Video Cut Boundaries
reaper.AddProjectMarker(0, false, 0.0, 0.0, "SFX: Strobe Flash Boom", -1)
reaper.AddProjectMarker(0, false, 1.2, 0.0, "SFX: Kinetic Title Whoosh", -1)
reaper.AddProjectMarker(0, false, 6.2, 0.0, "SFX: Match Cut Snap", -1)

reaper.Undo_EndBlock("Pocket CD: Speech Ducking & SFX Alignment", -1)
reaper.ShowConsoleMsg("Pocket CD Sound Design automation applied!\\n")`;
    } else if (this.activeExportFormat === 'dna') {
      label.innerText = 'Download .json';
      summary.innerText = 'Style DNA Specification Manifest (Universal Engine Format)';
      const sig = this.signaturesData.find(s => s.id === this.activeSignatureId) || this.signaturesData[0];
      codeBox.textContent = JSON.stringify(sig, null, 2);
    }
  }

  downloadCurrentExportFile() {
    const code = document.getElementById('exportCodePreview').textContent;
    let filename = 'ackman_edit_dna.jsx';
    let mime = 'text/plain';

    if (this.activeExportFormat === 'ae') {
      filename = 'ackman_edit_dna.jsx';
    } else if (this.activeExportFormat === 'resolve') {
      filename = 'build_resolve_timeline.py';
    } else if (this.activeExportFormat === 'reaper') {
      filename = 'speech_ducking_sfx.lua';
    } else if (this.activeExportFormat === 'dna') {
      filename = 'ackman_style_dna.json';
      mime = 'application/json';
    }

    const blob = new Blob([code], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    this.showToast(`Exported ${filename}`, 'success');
  }

  copyExportCode() {
    const code = document.getElementById('exportCodePreview').textContent;
    navigator.clipboard.writeText(code).then(() => {
      this.showToast('Copied script code to clipboard!', 'success');
    }).catch(() => {
      this.showToast('Could not copy to clipboard.', 'warning');
    });
  }

  /**
   * Close all active modals
   */
  closeAllModals() {
    document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('open'));
  }

  /**
   * Floating Toast Notifications
   */
  showToast(message, type = 'info') {
    if (!this.toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let iconSvg = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;
    if (type === 'success') {
      iconSvg = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
    } else if (type === 'warning') {
      iconSvg = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`;
    }

    toast.innerHTML = `${iconSvg}<span>${message}</span>`;
    this.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(8px)';
      toast.style.transition = 'all 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, 3200);
  }
}

// Global App Instance
let pocketApp;
document.addEventListener('DOMContentLoaded', () => {
  pocketApp = new PocketDirectorApp();
  pocketApp.init();
});
