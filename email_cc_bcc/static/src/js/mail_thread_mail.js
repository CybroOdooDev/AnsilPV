/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { escapeAndCompactTextContent } from '@mail/js/utils';

registerPatch({
    name: 'ComposerView',
    lifecycleHooks: {
        _created() {
            this._super();
            this.mail_partner_type = [];
        },
    },
    recordMethods: {
        onChangeMailType(ev, partner){
            let exist = this.mail_partner_type.filter((val) => val.partner_id == partner.id)
            if(exist.length){
                this.mail_partner_type.splice(this.mail_partner_type.indexOf(exist))
            }
            this.mail_partner_type.push({
                partner_id: partner.id,
                type: ev.target.value,
                email: partner.email
            })
        },
        onChangeCheckFollower(ev, partner){
            let exist = this.mail_partner_type.filter((val) => val.partner_id == partner.id)
            if(exist.length){
                this.mail_partner_type.splice(this.mail_partner_type.indexOf(exist))
            }
            if(ev.target.checked){
                this.mail_partner_type.push({
                    partner_id: partner.id,
                    type: 'cc',
                    email: partner.email
                })
            }
        },
        /**
         * Called when clicking on "send" button.
         */
        async onClickSend() {
            if(this.composer.isLog){
                this.sendMessage();
                this.update({ doFocus: true });
            } else {
                this.openFullComposerCcBcc()
            }
        },
        async openFullComposerCcBcc(){
            let email_cc = this.mail_partner_type.map((val) => {
                if(val.type == 'cc'){
                    return val.email
                }
            })
            let email_bcc = this.mail_partner_type.map((val) => {
                if(val.type == 'bcc'){
                    return val.email
                }
            })
            let context = {
                default_attachment_ids: this.composer.attachments.map(attachment => attachment.id),
                default_body: escapeAndCompactTextContent(this.composer.textInputContent),
                default_is_log: this.composer.isLog,
                default_model: this.composer.activeThread.model,
                default_partner_ids: this.composer.recipients.map(partner => partner.id),
                default_res_id: this.composer.activeThread.id,
                mail_post_autofollow: this.composer.activeThread.hasWriteAccess,
            }
            if(email_cc){
                context.default_email_cc = email_cc.filter((val) => val != undefined).join(', ')
            }
            if(email_bcc){
                context.default_email_bcc = email_bcc.filter((val) => val != undefined).join(', ')
            }
            const action = {
                type: 'ir.actions.act_window',
                res_model: 'mail.compose.message',
                view_mode: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: context,
            };
            const composer = this.composer;
            const options = {
                onClose: () => {
                    if (!composer.exists()) {
                        return;
                    }
                    composer._reset();
                    if (composer.activeThread) {
                        composer.activeThread.fetchData(['messages']);
                    }
                },
            };
            await this.env.services.action.doAction(action, options);
        }
    },
})