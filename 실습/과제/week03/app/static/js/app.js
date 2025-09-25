// 전역 유틸리티 함수들
class AppUtils {
    // 날짜 포맷팅
    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
    
    // 상대적 시간 표시
    static timeAgo(dateString) {
        const now = new Date();
        const date = new Date(dateString);
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return '방금 전';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}분 전`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}시간 전`;
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}일 전`;
        
        return this.formatDate(dateString);
    }
    
    // 텍스트 길이 제한
    static truncateText(text, maxLength = 100) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    // 태그 문자열을 배열로 변환
    static parseTags(tagsString) {
        if (!tagsString) return [];
        return tagsString.split(',').map(tag => tag.trim()).filter(tag => tag);
    }
    
    // 배열을 태그 문자열로 변환
    static tagsToString(tagsArray) {
        if (!Array.isArray(tagsArray)) return '';
        return tagsArray.join(', ');
    }
    
    // API 에러 처리
    static async handleApiResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: '알 수 없는 오류가 발생했습니다.' }));
            throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    }
    
    // 로딩 상태 표시
    static showLoading(element) {
        const originalContent = element.innerHTML;
        element.innerHTML = '<i class="loading"></i> 처리중...';
        element.disabled = true;
        
        return () => {
            element.innerHTML = originalContent;
            element.disabled = false;
        };
    }
    
    // 토스트 알림
    static showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // 토스트 스타일
        Object.assign(toast.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '9999',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease',
            maxWidth: '300px'
        });
        
        // 타입별 배경색
        const colors = {
            success: 'linear-gradient(45deg, #56ab2f, #a8e6cf)',
            error: 'linear-gradient(45deg, #ff6b6b, #ee5a6f)',
            warning: 'linear-gradient(45deg, #ffc107, #ffed4a)',
            info: 'linear-gradient(45deg, #667eea, #764ba2)'
        };
        toast.style.background = colors[type] || colors.info;
        
        document.body.appendChild(toast);
        
        // 애니메이션
        setTimeout(() => toast.style.transform = 'translateX(0)', 100);
        
        // 자동 제거
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }
    
    // 확인 대화상자
    static async confirmDialog(message, title = '확인') {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.style.display = 'block';
            
            modal.innerHTML = `
                <div class="modal-content" style="max-width: 400px;">
                    <div class="modal-header">
                        <h3>${title}</h3>
                    </div>
                    <div style="padding: 2rem;">
                        <p style="margin-bottom: 2rem; color: #666;">${message}</p>
                        <div class="form-actions">
                            <button class="btn btn-secondary" onclick="resolveConfirm(false)">취소</button>
                            <button class="btn btn-danger" onclick="resolveConfirm(true)">확인</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            window.resolveConfirm = (result) => {
                document.body.removeChild(modal);
                delete window.resolveConfirm;
                resolve(result);
            };
            
            // 모달 외부 클릭 시 취소
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    window.resolveConfirm(false);
                }
            });
        });
    }
}

// 키보드 단축키 관리
class KeyboardShortcuts {
    static init() {
        document.addEventListener('keydown', this.handleKeydown.bind(this));
    }
    
    static handleKeydown(e) {
        // Ctrl/Cmd + N: 새 메모/할일 추가
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            
            const currentPage = window.location.pathname;
            if (currentPage.includes('memos')) {
                if (typeof openMemoForm === 'function') openMemoForm();
            } else if (currentPage.includes('todos')) {
                if (typeof openTodoForm === 'function') openTodoForm();
            }
        }
        
        // ESC: 모달 닫기
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal[style*="display: block"]');
            modals.forEach(modal => {
                modal.style.display = 'none';
            });
        }
        
        // Ctrl/Cmd + F: 검색 포커스
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            const searchInput = document.querySelector('input[type="search"], input[placeholder*="검색"]');
            if (searchInput) {
                e.preventDefault();
                searchInput.focus();
                searchInput.select();
            }
        }
    }
}

// 로컬 스토리지 관리
class StorageManager {
    static set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.warn('로컬 스토리지 저장 실패:', error);
        }
    }
    
    static get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.warn('로컬 스토리지 읽기 실패:', error);
            return defaultValue;
        }
    }
    
    static remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.warn('로컬 스토리지 삭제 실패:', error);
        }
    }
    
    // 사용자 설정 저장/복원
    static saveUserPreferences() {
        const preferences = {
            theme: document.body.dataset.theme || 'light',
            language: document.documentElement.lang || 'ko'
        };
        this.set('userPreferences', preferences);
    }
    
    static loadUserPreferences() {
        const preferences = this.get('userPreferences', {});
        
        if (preferences.theme) {
            document.body.dataset.theme = preferences.theme;
        }
        
        if (preferences.language) {
            document.documentElement.lang = preferences.language;
        }
        
        return preferences;
    }
}

// 실시간 검색 디바운싱
class SearchDebouncer {
    constructor(callback, delay = 300) {
        this.callback = callback;
        this.delay = delay;
        this.timeoutId = null;
    }
    
    execute(...args) {
        clearTimeout(this.timeoutId);
        this.timeoutId = setTimeout(() => {
            this.callback.apply(this, args);
        }, this.delay);
    }
}

// 오프라인 상태 감지
class OfflineManager {
    static init() {
        this.updateOnlineStatus();
        window.addEventListener('online', this.updateOnlineStatus);
        window.addEventListener('offline', this.updateOnlineStatus);
    }
    
    static updateOnlineStatus() {
        const isOnline = navigator.onLine;
        
        if (isOnline) {
            AppUtils.showToast('온라인 상태입니다', 'success');
            // 오프라인 중 저장된 데이터 동기화 로직
            this.syncOfflineData();
        } else {
            AppUtils.showToast('오프라인 상태입니다', 'warning');
        }
        
        document.body.classList.toggle('offline', !isOnline);
    }
    
    static syncOfflineData() {
        // 오프라인 중 저장된 데이터가 있다면 서버와 동기화
        const offlineData = StorageManager.get('offlineData', []);
        
        if (offlineData.length > 0) {
            // 여기에 서버 동기화 로직 구현
            console.log('오프라인 데이터 동기화:', offlineData);
            StorageManager.remove('offlineData');
        }
    }
}

// DOM 로드 완료 후 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 키보드 단축키 초기화
    KeyboardShortcuts.init();
    
    // 오프라인 관리자 초기화
    OfflineManager.init();
    
    // 사용자 설정 로드
    StorageManager.loadUserPreferences();
    
    // 현재 페이지 네비게이션 활성화
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // 폼 자동 저장 (임시 저장 기능)
    const forms = document.querySelectorAll('form[data-auto-save]');
    forms.forEach(form => {
        const formId = form.id || 'unnamed-form';
        
        // 폼 입력 시 임시 저장
        form.addEventListener('input', AppUtils.debounce(() => {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            StorageManager.set(`draft-${formId}`, data);
        }, 1000));
        
        // 페이지 로드 시 임시 저장된 데이터 복원
        const draftData = StorageManager.get(`draft-${formId}`);
        if (draftData) {
            Object.entries(draftData).forEach(([name, value]) => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) field.value = value;
            });
        }
        
        // 폼 제출 시 임시 저장 데이터 삭제
        form.addEventListener('submit', () => {
            StorageManager.remove(`draft-${formId}`);
        });
    });
    
    // 툴팁 초기화
    initTooltips();
    
    // 이미지 지연 로딩
    initLazyLoading();
    
    // 접근성 개선
    initAccessibility();
});

// 디바운스 유틸리티
AppUtils.debounce = function(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// 툴팁 초기화
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const text = e.target.dataset.tooltip;
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 9999;
        pointer-events: none;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    e.target.tooltip = tooltip;
}

function hideTooltip(e) {
    if (e.target.tooltip) {
        document.body.removeChild(e.target.tooltip);
        delete e.target.tooltip;
    }
}

// 이미지 지연 로딩
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // 폴백: IntersectionObserver 미지원 시
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// 접근성 개선
function initAccessibility() {
    // 키보드 네비게이션 개선
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // ARIA 레이블 자동 설정
    const buttons = document.querySelectorAll('button:not([aria-label])');
    buttons.forEach(button => {
        const icon = button.querySelector('i');
        if (icon && !button.textContent.trim()) {
            // 아이콘만 있는 버튼에 ARIA 레이블 추가
            const iconClass = Array.from(icon.classList).find(c => c.startsWith('fa-'));
            if (iconClass) {
                const actionName = iconClass.replace('fa-', '').replace('-', ' ');
                button.setAttribute('aria-label', actionName);
            }
        }
    });
}

// Export for use in other scripts
window.AppUtils = AppUtils;
window.StorageManager = StorageManager;
window.SearchDebouncer = SearchDebouncer;