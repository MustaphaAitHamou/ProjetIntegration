describe('Users App E2E Flow', () => {
    it('crée, liste et supprime un utilisateur', () => {
      // Visite la page d'accueil
      cy.visit('/');
  
      // Remplit et soumet le formulaire
      cy.get('input[placeholder="Email"]').type('test@example.com');
      cy.get('input[placeholder="Password"]').type('password123');
      cy.contains('Add User').click();
  
      // Vérifie que l'utilisateur apparaît dans la liste
      cy.contains('test@example.com').should('be.visible');
  
      // Supprime l'utilisateur et vérifie sa disparition
      cy.contains('Delete').click();
      cy.contains('test@example.com').should('not.exist');
    });
  });