/**
 * Catalog UI Renderer
 * Renders hero catalog card, provenance badges, and price breakdown.
 */

class CatalogRenderer {
  static renderHeroCatalog(containerId, catalogData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const fields = catalogData.fields || [];
    const getField = (name) => fields.find(f => f.field_name === name) || {};

    const nameField = getField('product_name');
    const materialField = getField('primary_material');
    const craftField = getField('craft_category');
    const hoursField = getField('work_hours');
    const expField = getField('experience_years');

    const pEst = catalogData.price_estimate || {};

    container.innerHTML = `
      <div class="catalog-card">
        <div class="catalog-img-container">
          <img src="/assets/images/sample_teak_carving.jpg" alt="Craft Artwork" class="catalog-img" />
        </div>
        <div class="catalog-body">
          <div class="catalog-title">${catalogData.product_name || 'Handcarved Teak Sculpture'}</div>
          
          <div class="catalog-grid">
            <div class="catalog-meta-item">
              <div class="catalog-meta-label">
                <span>Material</span>
                <span class="badge-provenance ${this.getBadgeClass(materialField.source)}">${materialField.source || 'ARTISAN'}</span>
              </div>
              <div class="catalog-meta-value">${catalogData.primary_material || 'Teak Wood'}</div>
            </div>

            <div class="catalog-meta-item">
              <div class="catalog-meta-label">
                <span>Craft</span>
                <span class="badge-provenance ${this.getBadgeClass(craftField.source)}">${craftField.source || 'AI_VISION'}</span>
              </div>
              <div class="catalog-meta-value">${catalogData.craft_category || 'Wood Craft'}</div>
            </div>

            <div class="catalog-meta-item">
              <div class="catalog-meta-label">
                <span>Work Time</span>
                <span class="badge-provenance ${this.getBadgeClass(hoursField.source)}">${hoursField.source || 'ARTISAN'}</span>
              </div>
              <div class="catalog-meta-value">${catalogData.work_hours || 20} Hours</div>
            </div>

            <div class="catalog-meta-item">
              <div class="catalog-meta-label">
                <span>Experience</span>
                <span class="badge-provenance ${this.getBadgeClass(expField.source)}">${expField.source || 'ARTISAN'}</span>
              </div>
              <div class="catalog-meta-value">${catalogData.experience_years || 25} Years</div>
            </div>
          </div>

          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.4; margin-top: 10px;">
            ${catalogData.description || 'Intricately carved wooden sculpture created with traditional techniques.'}
          </p>

          <div class="price-hero-box">
            <div class="price-title">AI Suggested Fair Price</div>
            <div class="price-value">₹${pEst.suggested_min ? pEst.suggested_min.toLocaleString() : '4,500'} – ₹${pEst.suggested_max ? pEst.suggested_max.toLocaleString() : '5,500'}</div>
            <div class="price-explanation">
              ${window.artaApp && window.artaApp.language === 'ta' ? pEst.explanation_ta : pEst.explanation_en}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  static getBadgeClass(source) {
    switch (source) {
      case 'ARTISAN': return 'badge-artisan';
      case 'AI_VISION': return 'badge-ai-vision';
      case 'AI_INFERENCE':
      case 'AI_GENERATED': return 'badge-ai-suggested';
      default: return 'badge-confirmed';
    }
  }
}

window.CatalogRenderer = CatalogRenderer;
